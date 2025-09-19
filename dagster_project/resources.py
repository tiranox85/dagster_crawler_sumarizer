from dagster import resource
from sqlalchemy import create_engine
import requests
import hashlib
import os
import openai


@resource(config_schema={'db_url': str})
def db_resource(init_context):
    engine = create_engine(init_context.resource_config['db_url'])
    return engine


# dagster_project/resources.py (scraper_resource section)
from dagster import resource
import requests

@resource(config_schema={'actor_id': str, 'api_token': str, 'default_url': str})
def scraper_resource(init_context):
    actor_id = init_context.resource_config['actor_id']
    api_token = init_context.resource_config['api_token']
    base_url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={api_token}"

    class ScraperClient:
        def __init__(self, url):
            self.url = url

        def fetch_latest(self, n=50):
            run_input = {
                "startUrls": [{"url": "https://www.sec.gov/news/pressreleases"}],
                "maxPagesPerCrawl": 1
            }
            try:
                run = requests.post(self.url, json=run_input)
                run.raise_for_status()
                run_id = run.json()['data']['id']

                dataset_url = f"https://api.apify.com/v2/datasets/{run_id}/items?token={api_token}&limit={n}"
                items_resp = requests.get(dataset_url)
                items_resp.raise_for_status()

                items = []
                for it in items_resp.json():
                    url = it.get('url') or it.get('link')
                    items.append({
                        'url': url,
                        'title': it.get('title'),
                        'published_at': it.get('date') or None,
                        'raw': it
                    })
                return items

            except requests.exceptions.HTTPError as e:
                init_context.log.warning(
                    f"Apify call failed ({e.response.status_code}). Falling back to mock data."
                )

            except Exception as e:
                init_context.log.warning(f"Unexpected error calling Apify: {e}. Using mock data.")

            # Fallback mock data
            mock_items = [
                {
                    "url": f"https://www.sec.gov/news/pressrelease-{i+1}",
                    "title": f"Mock Press Release {i+1}",
                    "published_at": "2025-09-19",
                    "raw": {}
                }
                for i in range(n)
            ]
            return mock_items

    return ScraperClient(base_url)


@resource(config_schema={'api_key': str, 'model': str})
def llm_resource(init_context):
    api_key = init_context.resource_config['api_key']
    model = init_context.resource_config['model']
    client = openai.OpenAI(api_key=api_key)

    class LLMClient:
        def __init__(self, model):
            self.model = model

        def summarize(self, text):
            prompt = f"""
            Summarize the article into EXACTLY 3 bullet points, total <= 50 words.
            - Each bullet should be one short sentence.
            - Use neutral factual tone.

            Article:
            {text}
            """
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return {'model': self.model, 'summary': response.choices[0].message.content.strip()}

    return LLMClient(model)

