# Staged Approach

## Metadata

- **Type**: BestPractice
- **Use Case**: AI-assisted automation, batch processing, destructive operations
- **Created**: 2026-02-21
- **Source**: 2026-01-07 observation record

---

## Core Framework

Break complex automation tasks into three stages:

```
Stage 1: Data collection -> Stage 2: Batch processing -> Stage 3: Confirmation and publication
```

### Stage 1: Data Collection

- Fully pull source data locally
- Isolate from the online system
- Move to the next stage only after data has been written to disk
- Goal: ensure later processing has a stable data foundation

### Stage 2: Batch Processing

- Call AI in the local environment
- Stay fully isolated from the online system
- Make it repeatable and rollbackable
- Goal: complete AI nondeterministic operations inside a safe sandbox

### Stage 3: Confirmation and Publication

- Human review of processing results
- One-click publish or batch apply
- Record a change log
- Goal: keep human judgment as the final line of defense

---

## Core Principles

### Isolation-Processing-Verification Loop

```
Online environment <-> Local sandbox <-> Human confirmation
        |                  |                 |
      read-only         AI operations     publish decision
```

### Dry Run First

**Always perform a dry run before any destructive operation.**

Destructive operations include:
- File overwrite/deletion
- Database writes
- API POST/PUT/DELETE
- Email/message sending
- Any irreversible operation

Dry run checklist:
- [ ] Confirm operation scope (which files/records are affected)
- [ ] Confirm operation content (what the exact changes are)
- [ ] Confirm rollback is possible (backup or version control exists)
- [ ] Confirm execution environment (not production)

---

## Typical Use Cases

### Content Translation and Publication

1. Stage 1: Pull content to be translated locally
2. Stage 2: Batch translate with AI and generate a preview
3. Stage 3: Publish with one click after human review

### Data Processing Pipeline

1. Stage 1: Export source data (CSV/JSON)
2. Stage 2: AI processing + validation
3. Stage 3: Import into the target system after confirmation

### Batch Code Modification

1. Stage 1: Create an independent branch
2. Stage 2: AI performs changes + local tests
3. Stage 3: Merge after review

---

## Relationship to Other Skills

- Works with the "outcome certainty" principle in `bestpractice_ai_programming_mindset.md`
- Works with parallel processing in `workflow_parallel_subagents.md`
- Works with the verification mechanism in `bestpractice_temporal_info_verification.md`

## Changelog

| Date | Change |
|------|--------|
| 2026-02-21 | Initial version, from the 2026-01-07 observation record |
