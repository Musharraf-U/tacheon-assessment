# Tacheon Assessment — Musharraf Usman

Assessment submission for the Data & AI Product Engineer role at Tacheon/Smacient.

---

## Task 1 — Product Scoping

Designed a marketing intelligence tool called **MarketLens** — a 4-screen flow (Upload → Transform → Validate → Output) that ingests raw marketing data, transforms it, validates quality, and exports insights.

**Deliverables:**
- `task1-product-scoping/product-brief.md` — product brief with problem statement, user personas, and feature scope
- `task1-product-scoping/readme.md` — key decisions and trade-offs
- `task1-product-scoping/wireframe/` — 4-screen wireframe screenshots (Upload → Transform → Validate → Output)

---

## Task 2 — Data Pipeline

Built an end-to-end Python pipeline that fetches live technology news from NewsAPI, transforms and enriches the articles, and loads them into Google BigQuery for SQL querying.

**Deliverables:**
- `task2-pipeline/pipeline.py` — fetch → transform → load pipeline
- `task2-pipeline/config.py` — all configuration in one place
- `task2-pipeline/requirements.txt` — dependencies
- `task2-pipeline/queries/summary.sql` — aggregated summary query
- `task2-pipeline/readme.md` — setup, usage, and production considerations

---

## Stack

Python · pandas · Google BigQuery · NewsAPI · HTML/CSS