from dagster import job
from dagster_project.assets.crawler import crawl_press_releases
from dagster_project.assets.summarizer import summarize_press_releases

@job
def full_pipeline():
    # Chain the crawler into the summarizer
    summarize_press_releases(crawl_press_releases())
