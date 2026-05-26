# Product Brief: Marketing Performance Intelligence Tool (v1)

## Problem Statement

The team currently answers the question *"How is our marketing performing across 
channels right now, and where should we be focusing?"* through a fully manual 
process — someone digs through exports from multiple platforms, pulls numbers, 
and stitches together a response by hand.

Time and dependency on a specific person are operational problems with operational 
fixes. The deeper, structural problem is **inconsistency** — the same underlying 
data produces different answers depending on who is doing the analysis, what 
transformations they apply, and how they interpret the numbers. No amount of extra 
resource or documentation fully solves this. It requires the transformation logic 
itself to be standardised and owned by a system, not a person.

This tool exists to solve that.

---

## Primary User: Internal Analyst

v1 is scoped exclusively for the internal analyst — the person currently doing the 
manual work.

Clients ask the same question, but they have different needs: higher-level framing, 
polished presentation, and a different trust model. Trying to serve both in v1 
would mean designing for two conflicting contexts simultaneously. The right path is 
to solve the internal pain first, validate the transformation engine, and then build 
a client-facing layer on top of a proven foundation.

---

## What the Tool Does in v1

The analyst's current workflow:
1. Export files manually from known platforms (Google Ads, Meta, email tools, CRM)
2. Open each file individually
3. Apply transformations by hand — inconsistently, depending on who's doing it
4. Stitch together a response or report

The tool replaces steps 2–4 with a consistent, repeatable process:

1. **Upload** — Analyst uploads one or more CSV/Excel exports from known source 
   platforms
2. **Transform** — The tool applies a standardised, pre-defined transformation 
   ruleset for each recognised source format: normalising column names, handling 
   date formats, resolving nulls, deduplicating, and computing derived metrics
3. **Validate** — The tool surfaces a data quality summary before the analyst 
   proceeds: input rows vs output rows, null counts, duplicates removed, failed 
   records, and validation mismatches. The analyst can inspect a before/after 
   preview and review transformation logs to verify the output themselves
4. **Output** — Clean, structured data ready for reporting or dashboard use, 
   with full reproducibility — the same input will always produce the same output

A successful interaction ends with the analyst having a clean, consistent dataset 
they can trust and act on, having spent minutes rather than the better part of a 
morning getting there.

---

## Architecture Decision: Ingestion Layer vs Transformation Engine

The ingestion layer (what formats the tool accepts and from which sources) is 
deliberately built as a **separate service** from the transformation engine (the 
logic that cleans and reshapes the data).

In v1, the ingestion layer handles a fixed set of known source formats — the 
platforms the team currently exports from. This is possible because we are building 
for internal analysts whose tools and export formats are already known.

Separating the two means that adding support for new data formats or sources in 
future is an ingestion problem, not an engine problem. The transformation logic 
remains stable and testable independently of how data enters the system.

---

## Trust Model

An internal tool that produces numbers the analyst cannot verify is not useful — 
it just moves the inconsistency problem one step earlier.

Trust is built through transparency:

- **Transformation logs** — a full record of what was applied to the data and why
- **Before/after preview** — the analyst can inspect raw vs transformed records
- **Data quality metrics** — row counts, null rates, duplicate removal counts, 
  failed records, and validation mismatches surfaced prominently before output
- **Error and warning visibility** — nothing fails silently; every issue is 
  surfaced with enough context to act on
- **Reproducibility** — the same file uploaded twice always produces the same 
  output. This is the single most important trust signal for an analytical tool

---

## What is Explicitly Out of Scope for v1

### Direct platform API integrations (Meta Ads, Google Analytics, etc.)
Not building this because v1's job is to validate the transformation engine. API 
integrations are a data ingestion feature — they change how data enters the system, 
not how it is processed. If the engine is not solid, pulling live data into it 
creates a faster path to wrong answers. Build the engine first. Add integrations 
when the foundation is proven.

### Support for arbitrary/unknown data formats
v1 accepts a fixed set of known source formats. Supporting arbitrary uploads 
requires a generalised parsing and schema-inference layer that is a significant 
build in itself. The internal analyst use case does not need this — their sources 
are known and stable.

### Client-facing output layer
Clients need a different presentation, different framing, and a different trust 
model (they cannot inspect raw data the way an internal analyst can). Building for 
clients in v1 means designing for two users at once. Post-v1.

### Automated scheduling or pipeline orchestration
The tool in v1 is analyst-initiated — a human uploads a file and runs the process. 
Automation is a natural v2 feature once the transformation logic is stable and 
trusted. Scheduling an untested pipeline just automates inconsistency at scale.

---

## What I Would Revisit with More Time

- **Schema registry** — a formalised way to define and version the expected schema 
  for each source format, rather than encoding it in transformation logic directly. 
  This would make adding new sources cleaner and more auditable.
- **User-defined transformation rules** — allowing analysts to configure lightweight 
  custom rules without touching code, within guardrails. This extends flexibility 
  without breaking consistency.
- **Output connectors** — rather than downloading a clean CSV, pushing output 
  directly to a shared location (BigQuery, Google Sheets, a BI tool) would remove 
  the last manual step.
- **Deeper client-facing design** — once v1 is validated internally, a proper 
  discovery session with clients to understand their specific reporting needs before 
  building that layer.