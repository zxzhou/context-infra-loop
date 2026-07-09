# Deep Research Workflow

## Metadata

- **Type**: Workflow
- **Use Case**: Deep, comprehensive, verifiable third-party research on a topic
- **Output Location**: `contexts/survey_sessions/`
- **Created**: 2026-02-19
- **Last Updated**: 2026-03-30

## Core Principles

1. **Incentive-aware verification**: information value depends on the source's incentive structure. Vendor narratives are useful, but they cannot verify themselves. Every major claim must be traced to independent evidence whose incentives are unrelated to the publisher.
2. **Cross-verification**: multiple subagents cover overlapping themes so disagreements and contradictions expose blind spots.
3. **Traceability**: preserve URLs for all citations, keep original excerpts for key references, and do not rely on summaries.
4. **Progressive focusing**: scan the whole picture first, extract claims, then verify deeply by dimension.
5. **One main deliverable + reusable artifacts**: one final report, with key intermediate artifacts stored in the session directory.
6. **Shared research spine, forked reader mode**: search, verification, and artifact retention are shared; before drafting, choose internal or external mode based on the reader.

## Source Tiers

In each research task, source credibility is not equal. Tier by incentive structure:

| Tier | Type | Signal Characteristics | How to Use |
|------|------|----------|----------|
| Tier 1 | Official vendor docs, blogs, case studies | Tells you how the product wants to be seen | Extract claims; do not use as verification evidence |
| Tier 2 | Press coverage, sponsored reviews, third-party reviews | Helps understand market positioning, but incentives still lean positive | Useful for market narrative; not independent evidence |
| Tier 3 | Independent developer blogs, HN/Reddit discussions, Stack Overflow | Stronger signal, but sampling is biased | Use as verification signal while accounting for community bias |
| Tier 4 | GitHub issues, migration stories, production post-mortems, commit history | Behavioral evidence rather than attitude; migration costs far more than posting praise | Highest credibility; use to verify claims and mark boundaries |

Evidence credibility in ascending order: attitude expression ("I think it is good") < use-case description < comparative decision record < migration stories < production post-mortems < code/commit-level evidence. Prioritize the latter half.

## Two Reader Modes

Distinguish modes by **whether the reader's context is known and thick**, not by channel.

**Mode A: Internal (decision memo driven by shared context)** applies when the reader is yourself or a collaborator with long-term shared context. Writing contract: do not repeat shared common knowledge; focus on unknowns that change the conclusion, points most likely to be challenged, and points that conflict with existing views; prioritize conclusions, evidence, open questions, and recommended actions.

**Mode B: External (publishable argument with zero assumed context)** applies when the reader is not a known person. Writing contract: explicitly answer why this matters; put the most useful judgment in the first few paragraphs; write key definitions, comparison frames, and qualifications on the page instead of leaving them for the reader to fill in.

After choosing external mode, answer a more fundamental question: **is this relevant to the target reader now, later, or probably not now?** For many research subjects, the real answer is the third: it has little direct relevance to most readers in the short term, but may matter long term. If so, the article's thesis must admit this directly instead of implying short-term value by stacking flashy examples. Admitting "not relevant now" is not the same as "not worth writing"; the reason to write may be precisely to help readers separate short-term noise from long-term signal.

Ask three questions before choosing a mode: (1) is this reader known and do they share thick context? (2) is the main value helping them decide faster, or helping them understand and believe? (3) can the report stand alone after private background is removed? Use internal mode for shared-context and fast-judgment work; use external mode for self-contained, distributable, persuasive work.

## Workflow

### Phase 1: Initial Scan + Claim Extraction

**Goal**: Understand the whole picture; separate vendor narrative, market narrative, and independent evidence; extract claims that need verification.

**Operations**:

1. Use Tavily for 2-3 searches covering:
   - Basic description of the research object (Tier 1 official information)
   - Market evaluation and media coverage (Tier 2 market narrative)
   - Criticism, controversy, and known issues (Tier 3-4 signals)
2. Summarize 3-5 dimensions for deeper research.
3. **Claim extraction**: list key claims from Tier 1-2 sources about the product/object (performance, use cases, cost, advantages, etc.). For each claim, mark the verification channel: in what kind of Tier 3-4 source could this claim be confirmed or falsified? Include the verification task in Phase 2 subagent prompts.

**Output**: Write to `tmp/<session_slug>/scratchpad.md`, including a claim extraction table:

```markdown
## Claim Extraction

| Claim | Source (Tier) | Verification Channel | Verification Status |
|-------|-------------|----------|----------|
| "zero-config, works out of the box" | Tier 1 official docs | Search GitHub issues for setup pain; search Reddit for migration stories | Pending |
| "lower cost than competitors" | Tier 1 official blog | Production post-mortem; independent benchmark | Pending |
```

### Phase 1.5: Prior Work Positioning (Required for Academic Paper Research)

**Trigger condition**: the research object is an academic paper, or the core evidence for the research topic is one paper or a group of papers. Skip this step for products, companies, or purely industry topics.

**Why this step matters**: a paper's Related Work and Contribution claims are self-interested. Authors position themselves as favorably as possible. Without reading prior work, you cannot tell whether a paper is inventing a new problem or using a good measurement to confirm something the field already sensed. That distinction directly determines the article's positioning: field survey, single-paper deep dive, or hybrid.

**Operations**:

1. Read the paper's Related Work / Background sections and extract:
   - Every cited prior work
   - How the authors position themselves against prior work
   - The specific incremental contributions the authors claim

2. Build a cited-work mapping table:

```markdown
| Prior Work | Year/Venue | What It Did | What It Did Not Do | Claimed Advantage of This Paper |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

3. For each cited cluster, externally verify what the prior work actually established (use Tavily to search original papers, blogs, or community discussions; do not rely on this paper's own description). Pay special attention to:
   - Whether prior work's actual scope is wider or narrower than this paper describes
   - Whether prior work already has independent verification or community reproduction
   - Whether this paper's "first to do X" claim is true

4. Based on this, answer two questions:

**Increment judgment**: what is genuinely new in this paper?
- Separate "facts already known in the field" from "facts newly added by this paper"
- Evaluate increment size: conceptual level (medium/large), empirical level (medium/large), practical level (meaningful/marginal)

**Positioning judgment**: what should this become?
- **A. Field survey**: prior work is already rich, this paper is one piece of the chain, and the target reader needs the whole picture
- **B. Single-paper deep dive**: this paper's increment is large and self-contained enough; prior work needs only 1-2 background paragraphs
- **C. Hybrid (recommended default)**: 30-40% field background + 60-70% focus on this paper. First explain why the layer this paper attacks differs from the layer prior work focused on, then use this paper's measurement/data as the main line

**Output**: Write `## Prior Work Positioning` into the scratchpad. If a subagent was launched for this step, also store the result in `tmp/<session_slug>/prior_work_survey.md`.

**Common mistakes**:
- Accepting the paper's Related Work as fact without externally verifying prior work's actual scope
- Assuming "many citations" means "the field is mature" — many citations may also mean the field is fragmented
- Treating "this paper is the first to measure X" as equivalent to "X did not exist before" — measurement and discovery are different contribution types

### Phase 2: Split and Parallel Research

**Goal**: Go deep from multiple angles while verifying the claims extracted in Phase 1.

**Splitting principles**:

Use 3-5 dimensions. Each dimension should do two things at once: cover a topic and verify specific claims. Dimensions must have at least 50% overlap so different agents can find different interpretations or contradictory conclusions about the same information.

**Design dimensions by evidence function**, not just by topic:

- Official narrative (Tier 1-2): product self-definition, official cases, pricing logic
- Independent usage experience (Tier 3): developer usage records, community discussion, comparative decisions
- Failures and boundaries (Tier 3-4): known issues, GitHub issues, limitations, criticism
- Migration behavior (Tier 4): records of users moving from or to competitors, and why

**Start subagents**:

Start 3-5 subagents at the same time, each owning one dimension. Use these types:

- `librarian` — preferred for external research, documents, open-source code, and official materials
- `deep` category — autonomous deep research, suitable for complex multi-source tasks

```
task(
  subagent_type="librarian",
  load_skills=[],
  description="Research XX dimension",
  run_in_background=true,
  prompt="[specific research-dimension prompt]"
)
```

Each subagent prompt must state:
1. The specific topic to research
2. The claims relevant to this dimension from Phase 1 claim extraction (requiring support or refutation in Tier 3-4 sources)
3. Return behavioral evidence first (migration, production issues, commit history), not attitude expression (positive/negative reviews)
4. Return URLs and original excerpts, not summaries
5. Other relevant dimensions it may cover to create overlap

The main thread organizes key conclusions, source indexes, and judgment process into artifact files in the session directory. It does not need to preserve raw output verbatim, but key information must not exist only in stdout.

**Tavily parameter preferences**:
- `max_results=6` (raise to 10 if coverage is insufficient)
- `search_depth="advanced"`
- `include_answer=false` (inspect results and original excerpts directly; do not rely on an aggregate answer)
- Enable `include_images` / `include_image_descriptions` as needed

### Phase 3: Integration and Cross-Verification

**Goal**: Identify contradictions, compare how claims behave across source tiers, and form credible conclusions.

**Operations**:

1. Compare subagent results, focusing on:
   - Information found by multiple agents -> higher confidence
   - Information from only one source -> mark source and flag for verification
   - Contradictory information -> mark explicitly and analyze why
2. For every Phase 1 claim, check verification status:
   - Independent evidence in Tier 3-4 sources -> mark verified and record source
   - Appears only in Tier 1-2 sources -> mark "vendor source only, not independently verified"; do not write as fact in the report
   - Tier 3-4 evidence contradicts Tier 1-2 -> defer to Tier 3-4 and record the contradiction
3. If a major contradiction appears, launch a targeted subagent for verification.

### Phase 4: Writing

After research Phase 1-3 is complete, enter writing. Choose the path based on target output:

**If the output is an external-facing analytical article** -> load `workflow_analytical_writing.md` and execute from Phase A. That skill contains the author's analytical lens catalog (Thesis Catalog), judgment-synthesis steps (lens matching -> genealogy tracing -> narrative reframe -> thesis formation), and writing rules.

**If the output is an internal memo** (for yourself or a collaborator with shared context) -> the full analytical-writing workflow is unnecessary. Write directly: show the conclusion and evidence that most affect the decision first; make unresolved points and next actions clear. Read `rules/COMMUNICATION.md` once before drafting.

**Shared format requirements** (both modes):
- Chinese Markdown
- Every citation must have a URL in Markdown link format, and must use an **absolute link** (starting with `https://`). Relative links work on yage.ai but point to the wrong address when published to third-party platforms such as Circle
- Preserve original excerpts for key citations, not just summaries
- If the final deliverable is an external article, important sources should appear as inline Markdown links in the body, not only piled at the end

**Difference between survey report and blog article**: this workflow produces a survey report stored in `contexts/survey_sessions/`. It is not a blog article. Do not add blog frontmatter or a Kit subscription script tag. If the user asks to publish to the blog, copy it separately to `contexts/blog/content/` and add frontmatter; that is a separate step.

**Delivery endpoint**: once the final MD file under `contexts/survey_sessions/` is written, the research delivery is complete. Do not automatically continue into publication flows (yage share, blog, Twitter, Circle, etc.). Only when the user explicitly asks to publish should you execute subsequent steps with the corresponding skill flow.

**Storage location**: `contexts/survey_sessions/<topic>_survey_YYYYMMDD.md`

**Recommended artifact directory**: `tmp/<session_slug>/`, containing at least:
- `scratchpad.md` (including the claim extraction table)
- `search_manifest.md` (including output file index, subagent locating method, and data coverage assessment)
- `search_notes.md` (as needed)
- `source_index.md` (as needed)

## Search Manifest Must Include Output File Index

```markdown
## Output File Index

| File | Path | Description |
|------|------|------|
| Scratchpad | `tmp/<session_slug>/scratchpad.md` | Main-thread research notes |
| Search Manifest | `tmp/<session_slug>/search_manifest.md` | This file |
| Final Report | `contexts/survey_sessions/<topic>_survey_YYYYMMDD.md` | Final report |

## Raw Subagent Outputs

| Agent | Session ID | URLs | Status |
|-------|-----------|------|------|
| Agent 1 | `ses_xxx` | 50+ | completed |
```

## URL Retention Rules

URLs must be retained for: direct citations, data sources (numbers/statistics/ratings), evaluation sources, and official information.

If the final deliverable is an external-facing article, the default requirement is: **important sources should appear as inline Markdown links in the body.** Do not keep links only in end references or only in the scratchpad / manifest. Readers should be able to jump out and verify judgments, facts, and quotations directly from the body.

```markdown
**Source description** (URL)
> Original excerpt

or

Someone commented on a platform (URL):
> "Original text"
> (upvotes X downvotes Y)
```

Avoid: citations without URLs ("someone said..."), or summaries without original excerpts.

If the research will later become an external article, do another check before drafting: does the final article itself actually retain these URLs, rather than keeping them only in research artifacts?

## Common Research Dimensions

| Research Object | Possible Dimensions |
|---------|-----------|
| Product/service | Feature evaluation, price comparison, user cases, negative feedback, competitor analysis |
| Course/training | Course content, instructor background, student reviews, price value, alternatives |
| Company/organization | Business model, market position, reputation, controversies, financial condition |
| Technology/tool | Technical principles, usage experience, applicable scenarios, limitations, alternatives |
| Opinion/framework | Degree of consensus, authority endorsement, opposition, actual implementation, timeline accuracy |

## Common Pitfalls

| Pitfall | Countermeasure |
|-----|------|
| Only finding positive information | Search explicitly for "criticism", "negative review", "scam", "overpriced" |
| Single source of information | Force subagents to find multiple independent sources |
| Over-summarizing and losing detail | Require original excerpts, not just summaries |
| Dimension split too clean with no overlap | Deliberately make boundaries fuzzy when designing dimensions |
| Subagent returns shallow information | Emphasize "deep", "specific", and "original text" in the prompt |
| Intermediate files pile up | Centralize under `tmp/<session_slug>/` and keep only key indexes and judgments |
| Wrong subagent type | Use `librarian` or `deep` for external research; use `explore` only for internal codebases |
| Research result becomes vendor-marketing summary | Extract claims in Phase 1, assign dimensions by evidence function in Phase 2, and check verification status in Phase 3 |

For common writing-stage failure modes (relevance does not land, demos treated as evidence, vague time dimension, research summary instead of author writing, etc.), see the failure-mode table in `workflow_analytical_writing.md`.
