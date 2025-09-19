from dagster import op
from hashlib import sha256
import json
from sqlalchemy import text


@op(required_resource_keys={'scraper', 'db'})
def crawl_press_releases(context, limit: int = 50):
    client = context.resources.scraper
    engine = context.resources.db
    items = client.fetch_latest(limit)
    with engine.begin() as conn:
        for it in items:
            if not it['url']:
                it['url'] = 'lorem-ipsum'
            url_hash = sha256(it['url'].encode('utf-8')).hexdigest()
            conn.execute(text("""
                              INSERT INTO press_releases (url, url_hash, title, published_at, raw_payload)
                              VALUES (:url, :url_hash, :title, :published_at, :raw_payload)
                                  ON CONFLICT (url_hash)
                DO UPDATE SET last_seen_at = now(), raw_payload = EXCLUDED.raw_payload
                              """), {
                             'url': it['url'],
                             'url_hash': url_hash,
                             'title': it.get('title'),
                             'published_at': it.get('published_at'),
                             'raw_payload': json.dumps(it.get('raw', {}))
                         })
    return len(items)
