# Cognitive Profile Extraction Workflow

## Metadata

- **Type**: Workflow
- **Use Case**: Extracting predictive cognitive profiles from unstructured conversation data (group chats, Slack, Discord, email, podcast transcripts, etc.)
- **Output**: A set of "axioms" — conditional trigger rules that can predict the target person's reaction direction, argumentative posture, and rhetorical moves on new topics
- **Dependencies**: [Parallel Subagent Workflow](./workflow_parallel_subagents.md), [Deep Research Workflow](./workflow_deep_research_survey.md)
- **Created**: 2026-03-13
- **Source**: Example observation project (8,139 WeChat messages -> 15 axioms, 89% predictive backtest)

---

## Model Guardrail

**Pre-execution check**: confirm whether the current model ID contains `opus`.

- **Is Opus** -> continue. Your context window is extremely valuable; your core capabilities are design, quality control, and writing. Delegate all research, data processing, and coding to subagents, and default to parallel execution. Writing — including axiom text, indexes, and final reports — must be done by you personally and must not be outsourced.
- **Is not Opus** -> pause and ask the user:

  > "This workflow is designed for Opus — the context window and writing ability of Opus are core assumptions of the process. The model you are currently using is not Opus. Do you confirm you want to continue? If this is a model-selection mistake, I recommend switching to Opus before starting."

---

## Core Principles

### 1. Parallelism + Delegation Is the First Principle

Opus's context window is scarce and should not be consumed by scanning and retrieval. Workflow division of labor:

| Role | Who Does It | Notes |
|------|------|------|
| **Plan** | Opus main agent | Research plan, dimension split, task boundaries for each iteration |
| **Execute** | Subagents (parallel) | Data scanning, keyword retrieval, counterexample hunting, statistical analysis |
| **Write** | Opus main agent | Axiom text, indexes, reports — conceptual consistency and unified style can only be guaranteed by one agent |
| **QA** | Opus main agent | Cross-check subagent results, find contradictions, judge convergence |

Subagent scheduling follows the rules in [Parallel Subagent Workflow](./workflow_parallel_subagents.md): parallelism <= 5, research overlap 30-50%, `run_in_background=true`.

### 2. Do Not Delegate Writing (Hard Constraint)

All text for final outputs — axiom definitions, indexes, methodology reports — must be written by Opus personally. Reasons:
- Conceptual consistency across axioms (the same phenomenon must not be phrased contradictorily across different axioms)
- Precision of cross-references (the tension V05 references in V07 must align on both sides)
- Unified style (15 axioms should read as if written by one person, not stitched together by 5 agents)

Subagents produce **raw research material**, not any part of the final draft.

### 3. Iterations Roll Dynamically

**Minimum floor**: 3 rounds (broad scan + deep verification + at least one pressure-test/finalization round).

**No fixed upper bound**, but before each round you must evaluate whether to continue (see "Convergence Criteria"). Empirical experience: 3-4 rounds is the common convergence point; after 5 rounds, marginal returns drop sharply and overfitting risk appears.

### 4. Axioms Are Conditional Trigger Rules, Not Absolute Laws

Every axiom should have counterexamples and boundary conditions. An axiom with no counterexamples is either too broad ("he cares about AI") or insufficiently tested (it looks perfect only because nobody looked seriously for counterexamples).

---

## Workflow

### Phase 0: Data Preparation

**Goal**: Convert raw data into a searchable set of target-person messages.

**Input requirements**:
- Text message collection from the target person
- Preferably with timestamps (necessary for temporal evolution analysis)
- Preferably with source labels — group name/channel name/conversation type (necessary for cross-source comparison)
- Optional: context-bearing version (each message includes the previous and next N messages from other people, used to understand interaction patterns)

**Preprocessing steps** (delegate to subagent):
1. Extract target-person messages from the raw format (filter by ID rather than display name, because display names may vary across groups)
2. Produce statistical summary: total message count, time span, message distribution by source
3. If there are multiple conversation sources, produce a context-bearing version

**Scale assessment -> choose verification tier**:

| Data Size | Recommended Axiom Count | Verification Tier | Notes |
|---------|-----------|---------|------|
| < 500 messages | 3-5 | Lightweight | Sparse data; skip pressure testing |
| 500-2000 messages | 5-8 | Standard | Simplified pressure test (mutual exclusivity + counterexamples; skip predictive backtest) |
| 2000-5000 messages | 8-12 | Standard+ | Simplified predictive backtest possible (3 topics) |
| 5000+ messages | 10-15 | Full | All three verification layers, including predictive backtest (5+ topics) |

**Semantic search preparation** (recommended): if data size is >= 1000 messages, build an embedding cache at this stage (see [Semantic Search Skill](./semantic_search.md)). Split messages into independent text files or chunks and run embedding once to build the cache. In later Phase 1/2 work, subagents can use semantic search instead of pure keyword grep — semantic search can find messages with different keywords but similar meanings, which is especially valuable for discovering implicit views and boundary cases.

**Phase 0 outputs**: data overview report, verification-tier decision, initial dimension hypotheses, embedding cache (if applicable).

---

### Phase 1: Broad Scan (R0)

**Goal**: Scan in parallel from five orthogonal dimensions and produce a candidate axiom pool.

**What Opus does (Plan)**:
1. Define 5 scan dimensions. Recommended defaults:

| Dimension | Focus | Typical Keywords |
|------|--------|-----------|
| Domain views | Core judgments in the target person's professional domain (technical, business, academic, etc.) | Varies by domain |
| Methodology preferences | How they work, decide, and evaluate | process, standard, method, principle |
| Values and positions | Social issues, ethical judgments, institutional preferences | fairness, efficiency, should, should not |
| Argumentative style | How they refute, persuade, and concede | refutation markers, concession markers |
| Language and expression patterns | Sentence preferences, analogy habits, emotion markers | frequent phrases, punctuation usage |

2. Write a prompt for each subagent specifying: search scope, output format (timestamp + source + original text + candidate axiom), and allowed overlap range
3. Launch 5 subagents in parallel (`run_in_background=true`)

**What subagents do (Execute)**:
- Scan all data and extract patterns by assigned dimension
- Produce 3-5 candidate axioms per dimension, each with 3+ timestamped pieces of evidence
- Mark cross-dimensional findings for cross-verification

**What Opus does (Consolidate)**:
1. Collect results from the 5 subagents
2. Merge overlapping candidate axioms (merge criterion: same underlying judgment, not similar wording)
3. Split candidate axioms that are too broad
4. Produce a **candidate axiom list** (expected 12-20 candidates) and **initial synthesis analysis**

---

### Phase 2: Deep Verification (R1)

**Goal**: Verify candidate axioms for stability, distinctiveness, and boundary conditions.

**What Opus does (Plan)**:
1. Design 5 verification tasks. Recommended defaults:

| Task | Goal | Method |
|------|------|------|
| Core verification | Deep evidence chains for the 3-5 highest-confidence candidates | Exhaustive search of related messages |
| Cross-source comparison | Differences in the same view across sources | Group by source and compare |
| Missing-pattern supplement | Topics or patterns R0 may have missed | Open-ended scan of keywords not covered in R0 |
| Style verification | Consistency of argumentative style and language patterns | Marker-word frequency stats + pattern matching |
| Time series | Temporal stability and evolution of views | Group by month/quarter and mark turning points |

2. **Key deduplication constraint**: tell every subagent "do not reuse evidence cited in the previous round." This single instruction most improves report quality.
3. Launch 5 subagents in parallel.

**What subagents do (Execute)**:
- Run deep verification according to the assigned task
- For each candidate axiom, provide confidence score (1-10), counterexample list, and boundary-condition suggestions

**What Opus does (Consolidate)**:
1. Cross-check findings across subagents
2. Update confidence and add boundary conditions for each candidate axiom
3. Eliminate low-confidence candidates (recommended threshold: < 6.0)
4. **Judge convergence**: should the workflow continue to Phase 3?

---

### Phase 3: Pressure Testing (R2)

**Applies when**: standard tier or above (data >= 500 messages).

**Goal**: Actively attack the axioms' weaknesses and test the predictive power of the overall framework.

**What Opus does (Plan)**: design 3-5 pressure-test tasks. Three core tasks:

#### 3a. Mutual Exclusivity Check

Check whether axioms logically contradict one another.

Operation: group axioms by relevance (3-4 per group) and have subagents check for mutual exclusivity within each group. Mutual exclusivity does not always need to be eliminated; it can be absorbed through layers such as "descriptive vs. normative" or "default mode vs. boundary mode." But the conflict level must be marked (1-10).

#### 3b. Counterexample Hunting

Explicitly require subagents to **actively look for messages that refute the axioms**.

Operation: find at least 2 counterexamples per axiom, and assign each counterexample a destructive-power score (1-10). Counterexamples are not a sign that the axiom failed; counterexamples that can be absorbed by boundary conditions make the axiom more precise.

#### 3c. Predictive Backtest (Full Version)

Test the axiom set as a predictor.

Operation (strict order):
1. Design 5-10 hypothetical topics (covering different axiom combinations)
2. **Without searching the raw data**, use the axioms to make prior predictions: position direction, argumentative strategy, likely analogies/phrases
3. Search the raw data for semantically similar real conversations
4. Compare prediction and actual data, then score consistency

**Improved backtest protocol** (optional, more credible but more expensive):
- Sample topics randomly from real data instead of letting the agent choose
- Use an **independent agent that did not participate in axiom creation** to judge consistency
- Score prediction confidence and consistency separately

**Known limitations** (must be disclosed in the report):
- Small samples (5-10 topics) are not statistically robust
- LLM judging LLM predictions has systematic bias
- Continuous scales (e.g. 89%) and binary scales (e.g. 60%) differ significantly; report both numbers when possible

**What Opus does (Consolidate)**:
1. Revise each axiom's boundary conditions and confidence based on pressure-test results
2. Mark the relationship graph among axioms (loops, tensions, orthogonal relationships)
3. **Judge convergence**: is an additional round needed?

---

### Phase 4+: Finalization (R3+)

**Goal**: Opus personally writes all axiom text.

**Hard constraint**: this phase is not delegated. All axiom text is written by Opus alone.

**Axiom file template**:

```markdown
# Number Title

## Core Statement
One sentence, independently quotable.

## Expansion
2-3 paragraphs. Explain the logic chain and the relationship to other axioms.

## Boundary Conditions
Where it weakens or does not apply. Include counterexamples and tensions found in R2.

## Representative Evidence
Original statements with timestamps and sources (3-5 items).

## Cross-Source Behavior
How the same view is expressed differently across sources.

## Confidence
1-10 score with brief rationale.
```

**Additional fields for style axioms**:
- **Scope / Default Mode**: state which contexts activate the style axiom and which contexts switch the mode

**Index file**:
- Quick-reference table of all axioms (number, title, core statement, confidence)
- Relationship graph among axioms (loops, tensions, orthogonal relationships)
- Summary of key pressure-test findings

**If pressure-test feedback requires major revision** (not just boundary-condition tweaks), add one more R3 -> R4 round: after revision, run another simplified pressure test to verify the revision, then finalize.

---

### Phase 5: Publish as Web Site (Only When Explicitly Requested)

**Do not publish proactively.** Finalization completes the task. Enter this phase only when the user explicitly says "publish", "put it online", or "give me a link."

The basic conversion flow is in [Share Report to Web](./share_report.md). The following are extra lessons for a **multi-page axiom site**:

**Structure**: index page (`index.html`) + one subpage per axiom. The index page lists all axioms in a table (number, title, core statement, confidence), with each title linking to its subpage. Each subpage has a "Back to index" navigation link at the top.

**Practical details**:
1. Add interpage links in the Markdown source first (`[V01](V01_xxx.html)`); pandoc preserves the links during conversion
2. Each HTML file should be standalone and self-contained (embed CSS with `--embed-resources`) without relying on external stylesheets, so every subpage can be opened independently
3. Upload the entire folder with rsync rather than file by file, preserving directory structure and links
4. After upload, verify HTTP 200 for the index page and at least 2 subpages with curl

**Delegation rule**: HTML conversion and upload can be delegated to a subagent, but the Markdown source for the index page (axiom relationship graph, summary text) must be written personally by Opus — that is writing, not mechanical conversion.

---

## Convergence Criteria

After each round, evaluate these four signals:

| Signal | Meaning |
|------|------|
| Revision instructions are directly actionable | Can revise without more data -> convergence is possible |
| Predictive power reaches usable level | Continuous score >= 80% -> the framework has captured the core structure |
| Counterexample types start repeating | New counterexamples are the same kinds as previous ones -> diminishing returns |
| Relationships among axioms are stable | No longer need additions, merges, or major restructuring -> structural convergence |

**If 3 of the 4 signals are satisfied, converge.** If 2 are satisfied, do one more lightweight verification round to confirm.

**Risk of over-iteration**: after 4-5 rounds, each revision can grind axioms from "generalizable cognitive patterns" into "exact fit to the training data." Prefer preserving some roughness over overfitting.

---

## Axiom Design Standards

A good axiom should satisfy:

1. **Persistence**: appears repeatedly across time periods and topics; not a one-off statement
2. **Distinctiveness**: specific to the target person, not common sense most people would say
3. **Predictiveness**: can predict their position and expression style on new topics
4. **Specificity**: supported by multiple original statements from multiple independent time points
5. **Non-redundancy**: axioms do not overlap; each covers a different aspect
6. **Boundedness**: marks where it weakens or does not apply

**Axiom types**: recommended split into two categories:
- **View axioms**: define "what position they will take"
- **Style axioms**: define "how they will express it"

**Merge vs. split judgment**: same underlying judgment -> merge (even if phrasing differs); orthogonal underlying logic -> keep as separate axioms (even if domains are close).

---

## Methodology Lessons

The following lessons come from the example project and apply to all cognitive profile extraction tasks:

### 1. Predictive Power Is the Ultimate Validation Standard

Evidence count and confidence scores are intermediate metrics. The final criterion for whether an axiom holds is whether it can predict reactions to new topics.

### 2. Counterexamples Are More Valuable Than Positive Examples

Actively seeking counterexamples, quantifying destructive power, and absorbing counterexamples through boundary conditions is more useful than piling up supporting evidence. An axiom without counterexample pressure testing is only an observation; after pressure testing, it becomes an axiom.

### 3. Axioms Should Anchor at a Stable Level of Judgment

When the target person starts questioning a specific method but keeps the higher-level concept, the axiom should anchor at the higher-level concept. For example, anchor on "verification is the control plane" rather than "TDD is the control plane" — the former absorbs methodology drift, while the latter will be broken by new data.

### 4. Cross-Source Comparison Separates "Real Views" from "Social Performance"

How the same person expresses themselves in different contexts reveals what is an underlying belief and what is audience adaptation. If a view appears in only one source, it may be a product of that context. If the direction is consistent across sources but expression varies, it is more likely to be a real position.

### 5. Time Series Separates "Beliefs" from "Statements"

Without time, you cannot distinguish stable views from momentary statements. The temporal evolution of a view is part of the axiom itself; record turning points and trajectories.

### 6. Emotional Deviation Must Be Quantified

When the target person deviates from axiom predictions in some contexts, quantify the deviation rate (for example, "strict metric 2%, aggregate damage 6.5/10") instead of vaguely saying "sometimes deviates."

### 7. Deduplication Constraints Improve Subagent Quality the Most

Tell subagents "do not reuse evidence cited in the previous round." This simple constraint significantly reduces redundancy and forces agents to find new evidence.

### 8. Style Axioms Are Default Strategy Clusters

Target people usually adapt to audiences. Style axioms describe default high-frequency patterns, not the only pattern. The axiom text must explicitly mark activation conditions and mode-switching contexts.

### 9. Convergence Signals Beat Fixed Rounds

Do not preset "do N rounds"; monitor convergence signals instead. Over-iteration has two costs: context-window consumption and overfitting.

---

## Pitfalls and Countermeasures

| Pitfall | Countermeasure |
|------|------|
| Axiom too broad ("he cares about AI") | Ask: what specific behavior can this predict? If none, it is not an axiom |
| Axiom too narrow ("he opposes TDD") | Lift it to a higher conceptual level |
| Evidence selection bias (only finding support) | Force hedging through R2 counterexample hunting |
| Concept inconsistency across axioms | Do not delegate writing; one person drafts the whole set |
| Treating reposted content as the person's own view | Distinguish "act of reposting" from "stance expressed about the reposted content" |
| Treating social-context statements as stable beliefs | Cross-source comparison + time-series verification |
| Inflated predictive backtest | Report both continuous and binary scales and disclose evaluator limitations |
| Over-iteration causing overfitting | Monitor convergence signals and stop when >=3 are satisfied |
| Subagent research is not deep enough | Require original excerpts + timestamps in prompts; do not accept pure summaries |
| Context window consumed by research | Strictly preserve the division: Plan/Write by main agent, Execute fully delegated |

---

## Scale and Cost Reference

| Data Size | Total Subagent Calls | Estimated Rounds |
|---------|-------------------|---------|
| < 500 messages | 10-12 | 2-3 rounds |
| 500-2000 messages | 12-15 | 3 rounds |
| 2000-5000 messages | 15-20 | 3-4 rounds |
| 5000+ messages | 18-25 | 3-5 rounds |

Five parallel subagents per round is the default configuration. Adjust to 3-7 depending on data size and dimension complexity.

---

## See Also

- [Semantic Search Skill](./semantic_search.md) — go beyond keyword matching and use embedding similarity to find semantically related messages
- [Parallel Subagent Workflow](./workflow_parallel_subagents.md) — execution rules for subagent scheduling
- [Deep Research Workflow](./workflow_deep_research_survey.md) — base architecture for multi-agent parallelism + cross-verification
- [Multi-Agent Parallel Analysis](./bestpractice_multi_agent_analysis.md) — 50% overlap and cross-verification methodology
- Example observation project (the original source for this skill) — `contexts/people/magong/`

---

## Changelog

| Date | Change |
|------|------|
| 2026-03-13 | Initial version, abstracted and generalized from the example observation project's methodology.md |
