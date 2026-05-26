# Task 1: Product Scoping

## Overview

This folder contains my product scoping work for the internal marketing performance 
tool. The full brief is in `product-brief.md`. This README summarises the key 
decisions I made and what I would revisit with more time.

---

## Key Decisions

**Scoping v1 to internal analysts only**
The same question gets asked by both internal team members and clients, but they 
are not the same user. Clients need polished presentation and a different trust 
model. Trying to serve both in v1 means designing for two conflicting contexts at 
once. I scoped v1 to the internal analyst because that is where the operational 
pain lives, and a validated internal tool is the right foundation for a client-
facing layer later.

**Framing inconsistency as the core problem — not time or dependency**
Time can be reduced by adding resources. Dependency can be mitigated through 
documentation. Inconsistency cannot be solved either way — it is structural. The 
same data producing different answers depending on who is analysing it is a trust 
problem, and trust is what this tool is ultimately restoring. Every design decision 
in the brief flows from this framing.

**Separating ingestion from transformation**
The ingestion layer (what file types and source formats the tool accepts) is built 
as a separate concern from the transformation engine (the logic that cleans and 
reshapes data). In v1, ingestion is intentionally narrow — fixed, known source 
formats from the platforms the team already uses. Isolating it means future format 
additions are an ingestion problem, not an engine problem. The core logic stays 
stable.

**Leaving API integrations out of v1**
Direct integrations with platforms like Meta Ads or Google Analytics are a natural 
ask, but they are an ingestion feature — they change how data enters the system, 
not how it is processed. v1's job is to prove the transformation engine works and 
can be trusted. Adding live data pulls before the engine is validated just creates 
a faster path to wrong answers.

---

## What I Would Revisit with More Time

- **Schema registry** — formalising how source schemas are defined and versioned, 
  rather than encoding them inside transformation logic
- **User-configurable rules** — letting analysts define lightweight custom 
  transformations within guardrails, without touching code
- **Output connectors** — pushing clean data directly to BigQuery, Google Sheets, 
  or a BI tool instead of a CSV download, removing the last manual step
- **Client-facing layer** — running a proper discovery session with clients before 
  designing their version, rather than assuming their needs mirror the analyst's