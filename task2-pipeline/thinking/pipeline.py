import requests
import pandas as pd
from datetime import datetime, timezone
from google.cloud import bigquery
from config import (
    PROJECT_ID, DATASET_ID, TABLE_ID, LOCATION,
    NEWS_API_KEY, NEWS_API_URL, NEWS_QUERY,
    NEWS_LANGUAGE, NEWS_PAGE_SIZE
)


def fetch_news() -> list:
    params = {
        "q": NEWS_QUERY,
        "language": NEWS_LANGUAGE,
        "pageSize": NEWS_PAGE_SIZE,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("status") != "ok":
        raise ValueError(f"NewsAPI error: {data.get('message')}")
    return data.get("articles", [])


def transform(articles: list) -> pd.DataFrame:
    records = []
    for a in articles:
        source = a.get("source") or {}
        records.append({
            "article_id": a.get("url", ""),
            "source_name": source.get("name", "unknown"),
            "author": a.get("author") or "unknown",
            "title": a.get("title") or "",
            "description": a.get("description") or "",
            "url": a.get("url") or "",
            "published_at": a.get("publishedAt") or None,
            "content_snippet": (a.get("content") or "")[:500],
            "ingested_at": datetime.now(timezone.utc)
        })

    df = pd.DataFrame(records)
    df["published_at"] = pd.to_datetime(df["published_at"], utc=True, errors="coerce")
    df["title_word_count"] = df["title"].str.split().str.len()
    df["has_description"] = df["description"].str.len() > 0
    df = df.drop_duplicates(subset=["article_id"])
    df = df.dropna(subset=["published_at"])
    return df


def load(df: pd.DataFrame) -> None:
    client = bigquery.Client(project=PROJECT_ID)

    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
    dataset_ref.location = LOCATION
    client.create_dataset(dataset_ref, exists_ok=True)
    print(f"Dataset ready: {DATASET_ID}")

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    schema = [
        bigquery.SchemaField("article_id", "STRING"),
        bigquery.SchemaField("source_name", "STRING"),
        bigquery.SchemaField("author", "STRING"),
        bigquery.SchemaField("title", "STRING"),
        bigquery.SchemaField("description", "STRING"),
        bigquery.SchemaField("url", "STRING"),
        bigquery.SchemaField("published_at", "TIMESTAMP"),
        bigquery.SchemaField("content_snippet", "STRING"),
        bigquery.SchemaField("title_word_count", "INTEGER"),
        bigquery.SchemaField("has_description", "BOOL"),
        bigquery.SchemaField("ingested_at", "TIMESTAMP"),
    ]
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_TRUNCATE"
    )
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
    print(f"Loaded {len(df)} rows → {table_ref}")


def run():
    print("Fetching news articles...")
    articles = fetch_news()
    print(f"Fetched {len(articles)} articles")

    print("Transforming...")
    df = transform(articles)
    print(df[["source_name", "title", "published_at"]].to_string(index=False))

    print("Loading to BigQuery...")
    load(df)
    print("Pipeline complete.")


if __name__ == "__main__":
    run()