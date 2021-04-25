import time
from functools import wraps
from typing import Tuple, List, Any, Iterable, Callable

import pandas as pd

from icd10.core.common import thread_pool
from icd10.core.loaders import generic_read
from icd10.core.logging import logger
from icd10.core.utils import split_df, map2starmap_adapter
from icd10.models import ResearchProject, ResearchItem, ICD10Item
from model.common import CATEGORIES_DF
from model.roberta.predict import predict


def start_project(file_url: str) -> ResearchProject:
    research_project = ResearchProject(project_file_url=file_url)
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
                research_project.status = 'F'
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
    thread_pool.map(map2starmap_adapter(populate_icd10_items), batches)
    logger.info(f"Project {research_project.id} (file: {research_project.project_file_url}) "
                f"completed successfully")
    research_project.status = 'C'
    research_project.save()


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
def populate_icd10_items(research_project: ResearchProject, df: pd.DataFrame):
    prediction = predict(df)
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
            ]
        )
        for index, row in df.iterrows()
    ]
    icd10_items = ICD10Item.objects.bulk_create(icd10_items)
    return icd10_items
