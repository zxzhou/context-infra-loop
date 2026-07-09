# Skill Writing Guide (Meta-Skill)

## Metadata

- **Type**: BestPractice
- **Use Case**: When creating or rewriting skill files
- **Created**: 2026-03-29

## What This File Is For

Skill files define capabilities for AI agents. A well-written skill lets an agent complete tasks reliably. A poorly written skill either turns the agent into a mechanical checklist runner, or lacks the key boundaries and acceptance criteria that prevent the agent from expanding in the wrong direction.

This file defines the core principles, acceptance criteria, and known pitfalls for writing a good skill. It is not a template, and it does not prescribe a specific section order.

## Core Principles

### Principle 1: Prefer Outcome Certainty over Process Certainty

The traditional approach is to break a task into steps: do this first, do that second, handle X this way. This gives certainty at the process level, which is equivalent to writing a script in natural language. The problem is that agents have reasoning ability and tool-calling ability; using them as scripts wastes those abilities. More importantly, step-by-step writing cannot cover long-tail corner cases, and corner cases are exactly where agents are stronger than scripts.

The alternative is to move certainty from the process to the result: define what the endpoint looks like and how to verify that the endpoint has been reached, then let the agent decide how to get there.

In practice, a skill file needs to answer these core questions:

1. **Goal**: What needs to be accomplished. Say it clearly in one sentence.
2. **Acceptance criteria**: What result counts as success. Write these concretely enough that an agent with no other context can decide whether it is done. If it cannot decide, the criteria are not specific enough.
3. **Available resources**: Which tools the agent may call, which files it may read, and which boundaries it must respect.
4. **Output specification**: The format, storage location, and schema of the deliverables.

These four elements are the skeleton of a skill file. Everything else, including methodology suggestions, domain knowledge, and historical experience, should orbit around them.

### Principle 2: Write Enabling Guidance, Not SOP

The reader of a skill file is a reasoning agent, and its context window is scarce. Every paragraph in the skill file should increase the probability that the agent completes the task, rather than consuming attention.

Methodology suggestions are useful, but they should appear as suggestions and constraints; the agent has the right to adjust based on the actual situation. For example, "analyze by industry segment" is a good suggestion because it gives an effective analytical lens, but if the agent faces a day with only one major macro news item, it should be free to skip grouping and analyze globally.

Known pitfalls and traps must be written down, because these are things the agent is unlikely to discover on its own. One concrete record of a real failure is more valuable than ten generic methodology notes.

Two tests can help decide whether a paragraph belongs in a skill file. First, if you delete this paragraph, will the quality or probability of task completion drop? If not, delete it. Second, is this paragraph describing "how to do it" or "what done looks like"? Prefer the latter; keep the former only when it truly improves success probability.

## What a Skill File Should Include

The following are content areas a skill file usually needs to cover. Order and organization depend on the specific skill; you do not need to follow this list rigidly.

**Metadata.** Type (API Guide / Workflow / BestPractice / Tutorial), use case, output location, creation date, and update date.

**Goal and boundaries.** What the skill does and does not do. Boundaries are especially important: a clear "what it does not do" prevents drift better than a vague "what it does."

**Acceptance criteria.** Testable success conditions. Turn anything automatable into an automated check, such as running a script, checking a schema, or comparing against a threshold. For what cannot be automated, write human audit criteria. Each criterion should be specific enough for the agent to judge at runtime whether it has been met.

**Available resources and boundaries.** Tool list, file paths, external dependencies, and mandatory constraints. Emphasize what can be used, what must not be done, and which boundaries must not be crossed.

**Methodology suggestions.** Analytical frameworks, grouping strategies, or prioritization logic the agent may reference but does not have to follow rigidly. Be clear about which items are hard constraints and which are suggestions.

**Known pitfalls.** Traps encountered in previous iterations, with concrete failure symptoms and countermeasures. This is one of the highest-ROI parts of a skill file.

Special emphasis: **do not invent "possible pitfalls" at the beginning just to fill this section.** Known pitfalls should come from actual failures, rework, misjudgments, or real lessons from multi-round iterations. A new skill can absolutely omit this section in its first version, or leave only a short placeholder. Only when an error has actually happened and is likely to recur should it be written into the meta layer as a known pitfall.

**Output specification.** Format, schema, and storage path. If there is a JSON schema, a complete example is usually easier for an agent to understand than a schema description.

## Acceptance Criteria for This Meta-Skill

After writing a skill file, check it against the following standards.

**Outcome-oriented check.** Does the file contain clear, testable acceptance criteria? Can a new agent decide whether the task is complete after reading only this skill file? If not, the acceptance criteria are not specific enough.

**No redundant steps.** Does the file contain any step-by-step instructions ("first... second...")? If so, check whether each step is truly necessary. Most of the time it can be rewritten as goal + constraints. Keep ordering requirements only when sequence materially affects the result, for example "Y must be completed before X because X depends on Y's output."

**Pitfall coverage.** Does it record failure modes that have actually happened? If this is a brand-new skill, it can be left empty for now. Do not predict or fabricate pitfalls just to make the file look complete; adding them after real failures is more valuable.

**Boundary clarity.** Are the agent's key boundaries clear enough? For example: which tools can be used, what results count as out of bounds, which artifacts must be written to disk, and which constraints must not be violated. Vague boundaries make a skill lose its constraining power.

**Information density.** Is the file length reasonable? Does every paragraph increase the probability that the agent completes the task? If deleting a paragraph has no obvious impact on the result, consider deleting it.

## Common Pitfalls

| Pitfall | Symptom | Response |
|---------|---------|----------|
| Writing the skill as an SOP | The whole file is first step, second step; the agent becomes a mechanical executor | Rewrite it as goal + constraints + methodology suggestions |
| Vague acceptance criteria | "High-quality output," "deep analysis" | Replace with measurable conditions: "every judgment must cite item_id," "Brier Score beats naive baseline" |
| Over-constraining the process | The agent is required to use a specific method and fails when the method does not fit | Keep hard constraints at the outcome level; write methodology as suggestions |
| Missing boundary conditions | No explanation of what to do when data is missing, tools fail, or timeouts occur | At least cover the two degraded scenarios: "no data" and "tool unavailable" |
| Piling up background knowledge | Long domain introductions consume the agent's context window | Keep only background that directly affects task execution; reference the rest by file path |
| Wrapping error details away | A CLI/tool wraps the underlying error as a generic "something went wrong," losing status_code, response body, and other debug-critical details | Pass through raw error details (HTTP status, response body, exception type) so the AI agent can identify the root cause directly from the output. It is better to expose more information than to force a meaningless round of guessing |
| Forgetting to update INDEX.md | No one can find the new skill | Update `rules/skills/INDEX.md` immediately after writing the skill |

## Relationship to Existing Skills

Before writing a new skill, read `rules/skills/INDEX.md` to confirm there is no duplicate. If a similar skill already exists, modify it instead of creating a new one.

For format references, see `rules/skills/workflow_deep_research_survey.md` (a model for research skills) and `rules/skills/share_report.md` (a model for tool skills). Note that these are only format references; the core principles (outcome certainty, enabling rather than SOP) matter more than the format.
