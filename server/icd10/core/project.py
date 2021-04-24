import time
from typing import Tuple, List

import pandas as pd

from icd10.core.common import thread_pool
from icd10.core.loaders import generic_read
from icd10.core.logging import logger
from icd10.core.utils import split_df
from icd10.models import ResearchProject, ResearchItem, ICD10Item
from model.roberta.predict import predict


def start_project(file_url: str) -> ResearchProject:
    research_project = ResearchProject(project_file_url=file_url)
    research_project.save()
    logger.info(f"Starting research projet for file {file_url}")
    thread_pool.submit(run_project, research_project)
    return research_project


def run_project(research_project: ResearchProject):
    try:
        df = generic_read(research_project.project_file_url)
        _, df = populate_research_items(research_project, df)
        splits = split_df(df)
        thread_pool.map(populate_icd10_items, splits)
    except Exception as e:
        logger.exception(e)


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


def populate_icd10_items(df: pd.DataFrame):
    prediction = predict(df)
    df = df.join(prediction)
    icd10_items = [
        ICD10Item(
            item_id=row["id"],
            icd10_prediction=[
                {
                    "predicted_block_name": block_name,
                    "predicted_chapter_name": "value",
                    "predicted_chapter_code": "value",
                    "score": 0,
                    "block_description": "description",
                    "chapter_description": "same",
                    "link": "link"
                }
                for block_name in [
                    row["1st prediction"],
                    row["2nd prediction"],
                    row["3rd prediction"]
                ]
            ]
        )
        for index, row in df.iterrows()
    ]
    icd10_items = ICD10Item.objects.bulk_create(icd10_items)
    return icd10_items
