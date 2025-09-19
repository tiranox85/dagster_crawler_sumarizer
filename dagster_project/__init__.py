import os
from dagster import Definitions, ScheduleDefinition
from dagster_project.jobs import full_pipeline
from dagster_project.resources import db_resource, scraper_resource, llm_resource
from dagster_project.schedules import every_15m

DEFS = Definitions(
    jobs=[full_pipeline],
    schedules=[every_15m],
    resources={
        'db': db_resource.configured({'db_url': os.environ['DATABASE_URL']}),
        'scraper': scraper_resource.configured({
            'actor_id': os.environ['APIFY_ACTOR_ID'],
            'api_token': os.environ['APIFY_API_TOKEN'],
            'default_url': 'https://www.sec.gov/news/pressreleases'
        }),
        'llm': llm_resource.configured({
            'api_key': os.environ['OPENAI_API_KEY'],
            'model': 'gpt-4o-mini'
        })
    }
)
