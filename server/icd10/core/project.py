import time

from icd10.core.common import thread_pool
from icd10.models import ResearchProject, ResearchItem


def start_project(file_url: str) -> ResearchProject:
    research_project = ResearchProject(project_file_url=file_url)
    research_project.save()
    thread_pool.submit(run_project, research_project)
    return research_project


def run_project(research_project: ResearchProject):
    populate_research_items(research_project)
    thread_pool.submit()

def populate_research_items(research_project: ResearchProject):

    research_items = [
        ResearchItem(
            research_project=research_project,
            title=row["Title"],
            research_summary=row["Research Summary"],
            inclusion_criteria=row["Inclusion Criteria"]
        )
        for index, row in df.iterrows()
    ]