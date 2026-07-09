# Knowledge Flywheel Design Pattern

## Metadata

- **Type**: Workflow
- **Use Case**: Knowledge engineering, unstructured information processing, knowledge graph construction
- **Created**: 2026-02-21
- **Source**: Knowledge graph project practice

---

## Core Formula

**Dumb data + dumb methods + dumb models = refined knowledge**

Accept imperfect starting data, then gradually increase knowledge purity through an iterable system.

---

## Why Choose "Dumb Methods"?

### The Double Bind of Closed APIs

1. **Cost anxiety**: token-based billing discourages computationally intensive dumb methods
2. **Pace drag**: batch request response times are measured in hours, disrupting the fluid "think -> verify -> adjust" rhythm

### The Liberation of Local Deployment

After moving to locally deployed open-source models:
- Marginal cost approaches zero
- Large-scale iteration becomes feasible
- 5090 cluster + vLLM: a 32B model with 128k context needs only two GPUs

---

## Four-Step Flywheel Loop

```
Trigger -> call basic modules -> produce tiny progress -> refine
  ^                                      |
  +--------------------------------------+
```

### 1. Trigger

Identify a tiny, verifiable subproblem.

### 2. Call Basic Modules

Use simple, reliable atomic operations:
- Linear scan (instead of complex indexing)
- Semantic retrieval (embedding + cosine)
- Structured output (JSON/tables)

### 3. Produce Tiny Progress

Each loop must produce a measurable output:
- Extract an entity relationship
- Clarify an ambiguous concept
- Fill an information gap

### 4. Refine

Solidify the progress into the knowledge base so it becomes a basic module for the next round.

---

## Design Principles

### 1. Problem Decomposition

Break large problems into countless tiny, verifiable subproblems.

### 2. Independence

Each loop is an independent, logically clear process that does not rely on complex state.

### 3. High Success Rate

Design each subtask to succeed, avoiding avoidable frustration.

### 4. Convergence

The flywheel has a clear direction; every iteration moves closer to the goal.

### 5. Strategy for Breaking Static Points

Ways to break through a data flywheel "static point" (extremely rare data):
- Use VLMs for initial harvesting
- Use human-in-the-loop correction
- Form cold-start seed data

---

## Basic Module Examples

### Linear Scan

```python
# Do not over-design the index; get it running with a linear scan first
for chunk in text_chunks:
    if is_relevant(chunk, query):
        yield extract_info(chunk)
```

### Semantic Retrieval

```python
# embedding + cosine similarity is enough for most scenarios
def semantic_search(query, corpus, top_k=10):
    query_emb = embed(query)
    scores = [cosine(query_emb, doc_emb) for doc_emb in corpus_embs]
    return top_k_indices(scores)
```

### Structured Output

```python
# Force JSON output so later processing is easier
prompt = """
Extract person relationships from the following text and output JSON:
{"relations": [{"person_a": "...", "relation": "...", "person_b": "..."}]}
"""
```

---

## Model Selection Recommendations

### Recommended: Controllable Local Models

- **Qwen3-32B**: stability verified for knowledge engineering tasks; can output stably without special prompt tuning
- **Quantization**: with INT4 quantization, a 32B model with a 128k context window needs only two GPUs

### Not Recommended

- Expensive closed APIs (unless the budget is unlimited)
- Models that require complex prompt engineering to produce formatted output

---

## Pitfalls to Avoid

1. **Over-designing the index**: get it running with dumb methods first, then consider optimization
2. **Chasing perfect data**: accept an imperfect starting point and rely on flywheel iteration
3. **Complex pipelines**: every added step adds a failure point
4. **Premature optimization**: build 1.0 first, optimize later

---

## Practical Case

### Example: Structured Knowledge Graph

- **Input**: tens of millions of words from a novel
- **Output**: an interactively queryable structured knowledge graph
- **Method**: linear scan + semantic retrieval + four-step flywheel
- **Deployment**: *(your own deployment address)*
- **Cost**: first closed-API version was expensive; after moving to local deployment, marginal cost became zero

---

## See Also

- [T9. Data Strategy and MDP](../axioms/t09_data_strategy_mdp.md) — MDP concepts, breaking data flywheel static points, data sovereignty and accumulation

---

## Changelog

| Date | Change |
|------|------|
| 2026-02-21 | Promoted from OBSERVATIONS.md and organized into an independent skill |
