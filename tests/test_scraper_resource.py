import pytest
from dagster import build_resources

def test_scraper_fetch_latest(mock_scraper_resources):
    scraper = mock_scraper_resources
    results = scraper.fetch_latest(5)
    assert len(results) == 5
    assert all("url" in item and "title" in item for item in results)

def test_scraper_structure(mock_scraper_resources):
    scraper = mock_scraper_resources
    result = scraper.fetch_latest(1)[0]
    expected_keys = {"url", "title", "published_at", "raw"}
    assert expected_keys.issubset(result.keys())

def test_scraper_negative_limit(mock_scraper_resources):
    scraper = mock_scraper_resources
    result = scraper.fetch_latest(-5)
    assert result == []  # or whatever fallback scraper returns

