import pytest
from dagster import build_resources
from dagster_project.resources import db_resource, scraper_resource, llm_resource

@pytest.fixture
def temp_db_resources():
    """Provide a temporary DB resource for testing"""
    with build_resources(
            resources={
                'db': db_resource.configured({'db_url': "sqlite:///:memory:"})
            }
    ) as resources:
        # unpack tuple
        yield resources[0]

@pytest.fixture
def mock_scraper_resources():
    """Provide a mock scraper resource for testing"""
    with build_resources(
            resources={
                'scraper': scraper_resource.configured({
                    'actor_id': "dummy",
                    'api_token': "dummy",
                    'default_url': 'https://www.sec.gov/news/pressreleases'
                })
            }
    ) as resources:
        yield resources[0]  # unpack tuple

@pytest.fixture
def mock_llm_resources():
    """Provide a mock LLM resource for testing"""
    with build_resources(
            resources={
                'llm': llm_resource.configured({
                    'api_key': "dummy",
                    'model': "mock-model"
                })
            }
    ) as resources:
        yield resources[0]  # unpack tuple
