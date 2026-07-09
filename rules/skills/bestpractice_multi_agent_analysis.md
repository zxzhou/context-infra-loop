# Multi-Agent Parallel Analysis Best Practices

## Metadata

- **Type**: BestPractice
- **Applicable scenarios**: document analysis, research tasks, complex information synthesis
- **Created**: 2026-02-21
- **Source**: 2026-02-16 "4+4" multi-agent document-analysis experiment

---

## Experiment Background

Parallel analysis was performed on real-estate research documents using a 9-agent architecture: "4 comprehensive + 4 topical + 1 cross-validation."

Final output: 11 analysis JSON files (4,108 lines) and a visualization website.

---

## Core Findings
### The True Value of Multi-Agent: Context Window Isolation

The true value of a multi-agent framework is not role-play (PM/Dev/QA division), but **context window isolation**.

- The managing agent does not need to know low-level details such as syntax errors; it only needs high-level planning
- Each agent focuses on its own abstraction level, reducing information overload
- Blindly imitating human collaboration patterns, such as mechanical PM/Dev/QA division, is wrong AI-native design

### Keep 50% Overlap in Topic Partitioning

Do not split the task completely; let adjacent agents have 50% responsibility overlap.

Reasons:
- Overlap areas are the easiest places to miss things
- Overlap enables cross-validation
- Different agents may discover different angles in the same content

### Cross-Validation Finds Inconsistencies

Key inconsistencies found in the experiment:
- Contradictory garage-conversion feasibility assessments (Agent A considered it feasible; Agent B pointed out regulatory limits)
- Different interpretations of the 750-square-foot threshold across documents

Inconsistency is not a bug; it is a feature. It exposes contradictions and ambiguities in the information.

### Topical Depth Finds Cross-Dimensional Insights

Topical agents are more likely than comprehensive agents to find:
- cross-document patterns
- numeric thresholds, such as 750 square feet
- hidden constraints

---

## Recommended Architecture

### Small Tasks (<=3 Documents)

```
2-3 comprehensive agents (50% overlap)
```

### Medium Tasks (3-10 Documents)

```
3-4 comprehensive agents + 2-3 topical agents
```

### Large Tasks (>10 Documents)

```
4 comprehensive agents + 4 topical agents + 1 cross-validation agent
```

### Example Agent Division

| Type | Count | Responsibility |
|------|-------|----------------|
| Comprehensive | 4 | Each covers the full document set, with 50% overlap |
| Topical | 4 | Focus separately on finance / regulation / technology / market |
| Cross-validation | 1 | Compare the outputs of the first 8 agents and flag inconsistencies |

---

## Output Format

Structured JSON is recommended:

```json
{
  "agent_id": "comprehensive_1",
  "scope": ["doc1.md", "doc2.md", "doc3.md"],
  "findings": [
    {
      "topic": "topic",
      "summary": "summary",
      "evidence": "quoted source text",
      "confidence": "high/medium/low"
    }
  ],
  "cross_refs": ["related to finding X from comprehensive_2"]
}
```

---

## Relationship to Other Skills

This best practice is a **case study and extension** of [Parallel Subagent Workflow](./workflow_parallel_subagents.md): the workflow defines when to use it, core parameters, and the execution process; this document provides a methodological summary and output format from the "4+4" experiment.

- Use with the parallel execution framework in `workflow_parallel_subagents.md`
- Use with the research workflow in `workflow_deep_research_survey.md`
- Output can be used for Stage 2 processing in `bestpractice_staged_approach.md`

## Changelog
| Date | Change |
|------|--------|
| 2026-02-22 | Added core finding: context window isolation is the true value of multi-agent |
| 2026-02-21 | Initial version, from the 2026-02-16 experiment summary |
