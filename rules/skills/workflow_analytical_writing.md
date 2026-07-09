# Analytical Writing Workflow

## Metadata

- **Type**: Workflow
- **Use Case**: Turning research material into external-facing analytical writing with judgment
- **Prerequisites**: Phase 1-3 outputs from the deep research workflow (`workflow_deep_research_survey.md`)
- **Created**: 2026-04-28
- **Last Updated**: 2026-04-28

## When to Use

Load this skill after deep research is complete (the fact collection and verification work in Phase 1-3 is done) and you need to move from "verified material" to "an article with judgment." The core problem this skill solves is: the research material is sufficient, but the writing reads like an AI summary and lacks the author's analytical perspective and judgment framework.

**Relationship to the deep research skill**: the deep research skill handles information gathering and verification (Phase 1-3); this skill handles judgment synthesis and writing (Phase A-E). The reader-mode and writing material that used to live in Phase 3.5-4 of the deep research skill has moved here. After Phase 3, the research skill points to this workflow.

**Internal-mode articles** (for yourself or collaborators with shared context) usually do not need the full workflow. The value of internal mode is helping the other person decide faster; it does not require narrative reconstruction or genealogy tracing. Start directly from Phase D and make the conclusion, evidence, and open questions clear.

---

## Thesis Catalog: Core Analytical Lenses

These are the judgment frameworks the author repeatedly uses. When writing an external article, scan this list first and identify which lenses are relevant to the current topic. A typical article combines 1-3 lenses.

### L1: Feedback Loop Judgment

A system's capability ceiling depends on whether it can perceive its own outputs and correct itself. In AI systems, the most important factor is not model intelligence, but whether the model can see the consequences of its own behavior. Systems with complete loops can iterate on themselves; systems with missing loops can only rely on humans to fill the gap.

**Corresponding axioms**: A02 (amplifier), A04 (reliability is a management problem), M01 (closed-loop calibration)

**Typical applications**: three generations of creative AI evolution (Generation 1 cannot see rendered results; Generation 3 closes the loop through screenshots), the deployment crisis of agentic AI (the code runs but does not know whether it is correct), UE-bridge design (the core is viewport screenshot feedback)

**Trigger conditions**: the subject involves AI system reliability, degree of automation, or "why the demo is good but the real use case fails"

### L2: Bottleneck Migration Judgment

When the cost of one step drops sharply, the system bottleneck moves to the next slowest step. Optimizing a step that is no longer the bottleneck is pointless. In AI, once the cost of code generation approaches zero, the bottleneck moves to verification, judgment, and taste.

**Corresponding axioms**: X03 (efficiency is determined by the bottleneck), T05 (cognition is an asset; code is consumable)

**Typical applications**: the AI programming paradigm shift (testing becomes the bottleneck after coding becomes cheap), conclusions about creative AI (after execution friction disappears, competitive advantage shifts to taste), context infrastructure (after model intelligence crosses the threshold, context becomes the bottleneck)

**Trigger conditions**: when the subject claims to make X faster, cheaper, or easier, ask where the bottleneck moved

### L3: Consensus Ceiling Judgment

The default output of an LLM is consensus. Its training mechanism (next-token prediction + RLHF safety alignment) makes it regress to the mean. Differentiation and depth come from injecting non-consensus personal context, not from switching to a better model. Deep Research is really Wide Research.

**Corresponding axioms**: core thesis of the context infrastructure blog, A10 (familiarity beats raw intelligence)

**Typical applications**: context infrastructure (comparison experiment between two reports), harness engineering research (with context vs. without context), critique of Deep Research products

**Trigger conditions**: discussions of whether AI can do X, or any evaluation of AI output quality

### L4: Technical Genealogy Tracing

No new release appears out of nowhere. Tracing the previous generations lets you locate its real position on an evolutionary path and distinguish "genuinely new things" from "productization of an existing path." Usually this breaks into 2-4 generations, with each generation solving the core problem left by the previous one.

**Corresponding axioms**: M06 (connection beats isolated knowledge), A13 (three stages of technology adoption)

**Typical applications**: three generations of creative AI (script -> protocol -> closed loop), MCP evolution (research protocol -> collision with engineering reality -> dialect split), CLI-Anything positioning (bridge from the second generation to the third)

**Trigger conditions**: the subject is a newly released product, technology, or standard that needs to be positioned within an evolution

**How to operate**: first, identify the previous generations: what problem is this thing trying to solve? How did people solve it before? What was the previous generation's core limitation? Second, draw the evolutionary line: what did each generation solve, and what did it leave behind? Third, position the current object: which inherited problem does it solve, and what new problem does it leave? Fourth, judge the next step: based on the remaining problem, what might the next generation look like?

### L5: Gap Between Narrative and Reality

Media/vendor narratives usually focus on the wrong dimension. The article's core job is to redirect the reader's attention from the narrated dimension to the dimension that actually matters. That redirection itself is the thesis.

**Corresponding axioms**: T04 (data beats opinion), V02 (verifiability is the foundation of trust)

**Typical applications**: almost every external article has this move. Creative AI (the narrative focuses on "AI can do design"; the actual bottleneck is the feedback loop), Manus (the narrative focuses on "fully automatic AI agent"; the actual issue is verification and reliability), Claude Design vs. Figma (the narrative focuses on "competition"; the reality is two different user groups)

**Trigger conditions**: almost always needed. Ask yourself: what is most people's first reaction to this topic? What does that first reaction miss?

**How to operate**: first, extract the mainstream narrative: how do media, social networks, or vendors mainly interpret this event? Second, identify the dimension the narrative focuses on: where does this interpretation place attention? Third, identify the ignored dimension: what does this interpretation miss? Which dimensions matter more for actual judgment? Fourth, construct the redirection: the article's thesis is this redirection, "you think the point is X, but the key is Y."

### L6: Value Redistribution After Execution Friction Disappears

When tools remove execution-level friction, competitive advantage shifts from "who can execute faster" to "whose judgment is better." The value of tool mastery declines, and the value of taste and direction increases. This is L2 applied to the human dimension.

**Corresponding axioms**: T05 (cognition is an asset), A02 (AI is an amplifier, not a replacement)

**Typical applications**: creative AI conclusion sections (after execution friction disappears, creative direction and aesthetic taste become the core), AI programming cost-structure analysis, context infrastructure blog (the value of context rises while the value of model intelligence falls)

**Trigger conditions**: when the subject involves "AI making some category of work easier," ask where value moved

---

## Phase A: Lens Matching

**Input**: Outputs from research Phase 1-3 (scratchpad, verified claims, source index)

**Operations**:

1. Scan the Thesis Catalog (L1-L6 above) and check relevance to the current topic one by one. Mark each as: strongly relevant (will become the main line of argument), supporting (supports a point but is not the main line), or irrelevant.
2. Search the author's existing related writing. Look in `contexts/blog/`, `contexts/survey_sessions/`, and `rules/axioms/` for existing articles, research, and axioms directly related to the current topic. Record concrete file paths and relevant passages.
3. Check whether the author mentioned their own related thoughts or existing articles in conversation. If so, these are the strongest thesis anchors.

**Output**: Write `## Analytical Lens Selection` into the scratchpad:

```markdown
## Analytical Lens Selection

Main lenses: L4 (technical genealogy) + L5 (narrative gap)
Supporting lenses: L1 (feedback loop), L2 (bottleneck migration)
Irrelevant: L3 (consensus ceiling), L6 (value redistribution)

Existing related writing:
- contexts/blog/content/agentic-ai-crisis.md — original formulation of the feedback-loop argument
- axioms/x03 — general framework for bottleneck migration
- User mentioned in conversation: [specific quote]
```

## Phase B: Technical Genealogy Tracing

**Trigger condition**: Execute when L4 (technical genealogy) is marked strongly relevant or supporting in Phase A. Skip if irrelevant.

**Operations**:

1. Based on the research material, identify 2-4 generations that preceded the current event. For each generation, answer: what problem did it solve? What was its core limitation? Where was the break between it and the next generation?
2. Draw the generational evolution line and confirm the causal chain between generations: the previous generation's limitation directly gave rise to the next generation's core design.
3. Position the current event on the evolutionary line: which inherited problem does it solve, and what will it leave behind?

**Output**: Write `## Genealogy` into the scratchpad, including a generational table and evolutionary judgment.

## Phase C: Narrative Reframe

**Operations**:

1. **Extract mainstream narrative**: based on Tier 1-2 sources and media coverage, summarize most people's first reaction to the event in one sentence.
2. **Identify the dimension of focus**: where does this mainstream narrative place attention? What assumptions does it imply?
3. **Identify ignored dimensions**: based on Tier 3-4 evidence from the research and the analytical lenses selected in Phase A, which dimensions matter more for actual judgment but were ignored by the mainstream narrative?
4. **Construct the thesis**: the article's core argument is this redirection. Write it in one sentence: most people think [X], but the real key is [Y], because [evidence/mechanism].

**Note**: Not every article needs to "refute" the mainstream narrative. Sometimes the mainstream narrative is right but not deep enough. The article's job is to push one layer deeper rather than reverse direction. The thesis can redirect, deepen, or fill a missing dimension; it does not have to be oppositional.

**Output**: Write `## Narrative Reframe` into the scratchpad.

## Phase D: Thesis Formation and Skeleton

**Operations**:

1. Synthesize Phase A-C outputs into a complete thesis statement (2-3 sentences). The thesis must be understandable by a smart person who does not know the details; contain a specific judgment (not "this is complex and deserves attention"); and point to a judgment framework the reader can reuse elsewhere.

2. Decide reader mode and time dimension (judgments migrated from the deep research skill):
   - `mode`: `internal` or `external`
   - Who the target reader is
   - Time-dimension judgment: short-term relevance / long-term significance / relevance decision

3. Design the argument skeleton: list the argument path in 3-5 points. For each point, label which analytical lens it uses (L1-L6) and which evidence sources support it (which Tier 3-4 evidence supports this point).

4. Run a penetration check:
   - Does every main positive judgment have at least one independent Tier 3+ evidence source?
   - Is the time-dimension judgment stated directly in the opening?
   - Are demos distinguished from real-use scenarios?
   - Does the skeleton read like analysis written by the author using their own framework, or like an AI searched around and wrote a summary?

**Output**: `## Thesis & Skeleton` in the scratchpad.

## Phase E: Writing

**Required reading before writing**: `rules/COMMUNICATION.md`. Do not write first and compare afterward; load the rules before drafting. After-the-fact patches only catch literal keywords (dashes, certain stiff phrasing), not patronizing recommendation language, literal translation of English metaphors, or repetitive "very + adjective + colon" sentence shapes. Load it before writing so the sentences are right from the start. **If the output includes both Chinese and English versions**, after translating the English version, review it paragraph by paragraph against the translation-style rules in COMMUNICATION.md (literal passive voice, abstract use of expensive/cheap, narrow misuse of model/framework, missing transitions, etc.). Translation is where translationese appears most often; feeling that the Chinese draft already has the right style does not mean the translation still does.

**Control cognitive burden** (see axiom M11). The reader should receive no more than two new concepts in any paragraph. If a paragraph needs to introduce a new term or framework, first anchor it in a scenario or felt experience the reader already has, then name it. Do not introduce new concepts for three consecutive paragraphs without giving the reader room to digest. Test: read the article to someone matching the target reader profile. If they start drifting or rereading at a paragraph, the new-concept density there is probably too high.

**Shared format requirements**:
- Chinese Markdown
- All citations use absolute links (beginning with `https://`), not relative links
- Preserve original excerpts for key citations
- Important sources should appear as inline Markdown links in the body, not only piled at the end

**External-mode writing points**:

1. First let unfamiliar readers know "what it is and why it matters to me." Start the opening from a phenomenon readers can directly feel, not from technical terminology. Test: read the opening to a smart non-specialist. If they frown at the first paragraph and ask "what is this?", choose a different entry point.

2. If the Phase D time-dimension judgment is "not very relevant in the short term, possibly important long term," the opening must say that directly. Do not create false urgency by stacking flashy examples.

3. Prioritize intuition over technical detail. The article's goal is for readers to take away a reusable judgment framework, not to remember specific data. Technical detail is worth expanding only in three cases: (a) it is key evidence for the intuition, and without it the reader will doubt the judgment; (b) the reader is already fluent in the technical language, and detail is easier to understand than abstraction; (c) the detail itself is the article's subject. Test: read the article to a practitioner in an adjacent industry but outside this stack. If they can restate the core intuition but do not remember the exact numbers, the ratio is right.

4. **The analytical framework is an internal tool; it does not enter the finished article.** Thesis Catalog (L1-L6), axiom numbers, phase names, and terms like "narrative reframe" are all writing scaffolding and must not appear in the final article. Readers should feel a person with their own thinking style is doing analysis, not that a framework is being applied. Concretely: do not write "from the technical genealogy perspective"; directly describe the facts of the three-generation evolution. Do not write "the bottleneck migrated here"; directly say that after code became cheap, verification became the slowest step. Do not cite axiom numbers or names. The framework guides how you think, but readers only see the results of that thinking.

**Internal-mode writing points**:
- Help the reader decide faster
- Put the conclusion and evidence that most affect the decision up front
- Make unresolved points and next actions clear

**Difference between a survey report and a blog article**: the default output of this workflow is a survey report stored in `contexts/survey_sessions/`. It is not a blog article. Do not add Pelican frontmatter or a Kit subscription script. If the user asks to publish to the blog, copy it separately to `contexts/blog/content/` and add frontmatter.

**Delivery endpoint**: the final MD file is the delivery endpoint. Do not automatically run a publishing flow. Only execute the corresponding skill flow when the user explicitly asks.

---

## Common Failure Modes

| Failure Mode | Symptom | Fix |
|---------|------|------|
| Research summary rather than author writing | After reading, it feels like "an AI searched around and wrote a summary" | Phase A-C were skipped or superficial. Go back and do lens matching and narrative reframing |
| Relevance does not land | The reader does not know "what does this have to do with me" after the first few paragraphs | Start the opening from a felt phenomenon, not a technical concept |
| Demo treated as evidence | Flashy demos replace analysis of actual use scenarios | Distinguish "proves the technical ceiling" from "proves it can be used today" |
| Time dimension is vague | The article implies both "important now" and "still early" | The Phase D time-dimension judgment must be stated directly in the opening |
| Object-explainer | The piece always explains from the object outward rather than judging from the reader's situation | Change the subject from the analyzed object to "you" (the reader). If most paragraphs need rewriting, it is still object explanation |
| Opening starts from a technical concept | The first paragraph makes non-specialists frown | Switch to a felt phenomenon readers can directly understand |
| Analytical lens applied too mechanically | The article reads like a framework is being filled in | Lenses are implicit analytical tools, not explicit article structure. Let judgments emerge naturally |
| Genealogy becomes a chronology | Each generation receives equal attention with no argumentative priority | Genealogy serves the positioning of the current event; it is not a technology history. Only expand generations relevant to the current judgment |
| Internal framework leaks into the finished piece | The article contains phrases like "from L4 technical genealogy," axiom numbers, or "narrative reframe" | Thesis Catalog, axioms, and phase names are writing scaffolding; they should appear zero times in the final article |
| Cognitive burden too high | Multiple consecutive paragraphs introduce new concepts; readers drift or reread | No more than two new concepts per paragraph; anchor in an existing scenario before naming the concept |
