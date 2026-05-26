# Task 2 — Data Pipeline

## Overview

End-to-end pipeline that fetches live news articles from the NewsAPI, transforms and enriches them, and loads the results into BigQuery for querying.

**Use case:** Market signal ingestion for a marketing AI platform — tracking news volume, source distribution, and content trends across topics like `marketing technology`. Feeds downstream sentiment analysis and trend detection features like those in the MarketLens product (Task 1).

## Stack

| Layer | Tool |
|---|---|
| Source | NewsAPI REST API |
| Language | Python 3.10+ |
| Transform | pandas |
| Destination | Google BigQuery (Sandbox) |
| Query | Standard SQL |

## Setup

```bash
pip install -r requirements.txt
```

Authenticate with GCP:

```bash
gcloud auth application-default login
```

All configuration (API key, project ID, query terms) lives in `config.py` — nothing is hardcoded in the pipeline.

## Run

```bash
python pipeline.py
```

## Query

After loading, run the summary query in the BigQuery console or via CLI:

```bash
bq query --use_legacy_sql=false < queries/summary.sql
```

## File Structure

```
pipeline.py          # Fetch → Transform → Load
config.py            # All configuration
requirements.txt     # Dependencies
queries/
  summary.sql        # Article count and coverage by source
task2-pipeline/
  README.md          # This file
```

## Production Considerations

**Scheduling:** In production this runs daily via Cloud Scheduler → Cloud Run. The `ingested_at` timestamp enables full ingestion auditing.

**Write mode:** Currently `WRITE_TRUNCATE` (full refresh). Production would use `WRITE_APPEND` with a partitioned table on `published_at` and deduplication on `article_id` to build a historical archive.

**Error handling:** API rate limit errors (429) and BigQuery job failures should trigger retries with exponential backoff and alert via Slack or PagerDuty.

**Secrets:** The API key should be stored in Google Secret Manager in production — never committed to the repo. The key in `config.py` here is for assessment demonstration only.

**Schema evolution:** New enrichment fields (e.g. sentiment score, named entity tags) should be added via a migration script, not manual schema edits, to keep environments in sync.

**Monitoring:** Log row counts per run to a `pipeline_runs` audit table. Alert if count drops to zero — signals an API outage or query returning no results.

**Downstream use:** Enriched articles feed a sentiment scoring step (e.g. via Vertex AI or a lightweight VADER model) and a topic clustering model, both of which power the Validate and Output screens in MarketLens.