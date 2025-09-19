import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine
from dagster_project.resources import db_resource
from dagster import build_resources

@pytest.fixture
def temp_db_resources():
    # build_resources returns a tuple of resources in the order you pass them
    with build_resources(
            resources={
                'db': db_resource.configured({'db_url': "sqlite:///:memory:"})
            }
    ) as (db,):  # unpack tuple
        yield db  # this is the Engine

def test_db_resource_creation(temp_db_resources):
    db = temp_db_resources
    assert isinstance(db, Engine)

def test_db_can_insert(temp_db_resources):
    db = temp_db_resources
    with db.connect() as conn:
        conn.execute(text("""
                          CREATE TABLE press_releases (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          url TEXT NOT NULL
                          )
                          """))
        conn.execute(
            text("INSERT INTO press_releases (url) VALUES (:url)"),
            {"url": "https://example.com"}
        )
        conn.commit()

        result = conn.execute(text("SELECT url FROM press_releases"))
        rows = result.fetchall()
        assert rows[0][0] == "https://example.com"
