import json
import time
from datetime import datetime
from functools import wraps
from operator import itemgetter
from typing import Tuple, List, Any, Iterable, Callable

import pandas as pd

from icd10.core.common import thread_pool
from icd10.core.loaders import generic_read
from icd10.core.logging import logger
from icd10.core.utils import split_df, map2starmap_adapter, get_medical_terms
from icd10.models import ResearchProject, ResearchItem, ICD10Item, User
from medical_extraction.settings import ENGINE, BATCH_PREDICTION_COST


def start_project(file_url: str, user: User) -> ResearchProject:
    research_project = ResearchProject(project_file_url=file_url, user=user)
    research_project.save()
    logger.info(f"Starting research project {research_project.id} (file: {file_url})")
    thread_pool.submit(run_project, research_project)
    return research_project


class OnFailure:
    """ Decorator for wrapping any research project execution function and associate handlers
     with failures"""

    def __init__(self, fallback_value: Any = None, handlers: Iterable[Callable] = (),
                 message: str = "error"):
        self.fallback_value = fallback_value
        self.handlers = handlers
        self.message = message

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(research_project: ResearchProject, *args, **kwargs):
            try:
                return fn(research_project, *args, **kwargs)
            except Exception as e:
                logger.exception(f'"{fn.__name__}" {self.message}, '
                                 f'marking project {research_project.id} as failed')
                research_project.status = 'E'
                research_project.save()
                logger.debug(f"Running handlers...")
                for handler in self.handlers:
                    handler(research_project, exception=e, *args, **kwargs)
                logger.info(f'Using fallback value "{self.fallback_value}"')
                return self.fallback_value

        return wrapper


@OnFailure()
def run_project(research_project: ResearchProject):
    df = generic_read(research_project.project_file_url)
    _, df = populate_research_items(research_project, df)
    splits = split_df(df)
    batches = [(research_project, split) for split in splits]
    results = thread_pool.map(map2starmap_adapter(populate_icd10_items), batches)
    if any(map(lambda result: not isinstance(result, list), results)):
        research_project.status = 'E'
        research_project.end_date = datetime.now()
        research_project.save()
        logger.error(f"Project {research_project.id} (file: {research_project.project_file_url}) failed:\n"
                     "One of the mapped icd10 items failed, list of errors:")
        for result in results:
            if not isinstance(result, list):
                logger.error(result)
        return

    research_project.status = 'C'
    research_project.end_date = datetime.now()
    research_project.save()
    logger.info(f"Project {research_project.id} (file: {research_project.project_file_url}) "
                f"completed successfully")


@OnFailure()
def populate_research_items(research_project: ResearchProject, df: pd.DataFrame) \
        -> Tuple[List[ResearchItem], pd.DataFrame]:
    research_items = ResearchItem.objects.bulk_create([
        ResearchItem(
            project=research_project,
            title=row["Title"],
            research_summary=row["Research Summary"],
            inclusion_criteria=row["Inclusion Criteria"]
        )
        for index, row in df.iterrows()
    ])
    df["id"] = [research_item.id for research_item in research_items]
    return research_items, df


@OnFailure()
def populate_icd10_items(research_project: ResearchProject, df: pd.DataFrame) -> List[ICD10Item]:
    from model.common import CATEGORIES_DF
    from model.roberta.predict import predict
    user = research_project.user
    user.credits += BATCH_PREDICTION_COST
    user.save()
    logger.info(f"predicting chunk for project {research_project.id}...")
    prediction = predict(df)
    logger.info(f"chunk predicted for project {research_project.id}")
    df = df.join(prediction)
    icd10_items = [
        ICD10Item(
            item_id=row["id"],
            icd10_prediction=[
                {
                    "predicted_block_name": block_name,
                    "predicted_chapter_name": CATEGORIES_DF.loc[block_name]["chapter_name"],
                    "predicted_block_code": str(CATEGORIES_DF.loc[block_name]["block_code"]),
                    "predicted_chapter_code": str(CATEGORIES_DF.loc[block_name]["chapter_code"]),
                    "score": score,
                    "block_description": "description",
                    "chapter_description": "description",
                    "link": str(CATEGORIES_DF.loc[block_name]["link"])
                }
                for block_name, score in [
                    (row[f"block_name_{i}"], row[f"score_{i}"])
                    for i in range(row["top_k"])
                ]
            ],
            medical_terms=get_medical_terms(str(row["Title"]) + str(row["Research Summary"]) + str(row["Inclusion Criteria"]))
        )
        for index, row in df.iterrows()
    ]
    icd10_items = ICD10Item.objects.bulk_create(icd10_items)
    logger.info(f"icd10 items of chunk populated for project {research_project.id}")
    return icd10_items


def get_project_validated_data(project_id: int) -> pd.DataFrame:
    query = """
        select ir.title, ir.research_summary, ir.inclusion_criteria,
        iii.medical_terms, iii.icd10_validation
        from icd10_icd10item iii, icd10_researchitem ir 
        where ir.project_id =%(project_id)s and ir.id = iii.item_id and validated =true
    """
    df = pd.read_sql(query, ENGINE, params={"project_id": project_id})
    return df


def process_project_validated_data(df: pd.DataFrame) -> pd.DataFrame:
    from model.common import CATEGORIES_DF_BLOCK_CODE
    rows = []
    for index, row in df.iterrows():
        if row["icd10_validation"]:
            validation_codes = map(itemgetter("predicted_block_code"), row["icd10_validation"])
            validation_items = [
                {
                    "block_name": CATEGORIES_DF_BLOCK_CODE.loc[block_code]["block_name"],
                    "chapter_name": CATEGORIES_DF_BLOCK_CODE.loc[block_code]["chapter_name"],
                    "block_code": block_code,
                    "chapter_code": str(CATEGORIES_DF_BLOCK_CODE.loc[block_code]["chapter_code"])
                }
                for block_code in validation_codes
            ]
        del row["icd10_validation"]
        rows.extend([
            {
                **row,
                **validation_item
            }
            for validation_item in validation_items
        ])
    return pd.DataFrame(rows)
