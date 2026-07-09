# AI Product Design Principles

## Metadata

- **Type**: BestPractice
- **Applicable scenarios**: AI product design, interaction design, system architecture
- **Created**: 2026-02-22
- **Source**: Synthesis of multiple AI product practices

---

## The Fundamental Tension Between Linear Chat and Nonlinear Knowledge Work

### Nature of the Problem

The mainstream form of AI products is the "linear chat entry point" (ChatGPT, Claude Chat), but knowledge work is inherently nonlinear:
- thought jumps, branches, and backtracking
- parallel reference to multiple documents
- visual structures such as mind maps and outlines

### How the Tension Appears

- Users are forced to handle complex problems in a single thread
- Context accumulates linearly, making key information hard to locate
- Multiple lines of thought cannot be explored in parallel

### Design Implications

- Linear chat fits simple Q&A, not deep knowledge work
- Knowledge tools need to support nonlinear structures such as branches, links, and visualization
- Consider hybrid "conversation + document" forms

---

## Principle: Decouple Perception and Rules

### Architectural Decision

Strictly separate the "perception layer" from the "rules layer."

### Responsibilities of the Perception Layer

Output raw perception signals:
- lane position and line type
- vehicle heading angle
- road context

### Responsibilities of the Rules Layer

Make business judgments based on perception signals:
- what counts as "deviation"
- when to alert
- alert severity

### Benefits of Decoupling

1. **Fast iteration**: Product rules can be changed independently without retraining the model
2. **Personalization**: Different customers/regions can have different rules
3. **Auditability**: Rule changes are traceable while model output remains stable
4. **LLM integration**: Future LLMs can flexibly combine signals

### Applicable Scenarios

- Safety-critical systems that require deterministic rules
- Multi-market / multi-customer products that require personalization
- Business logic that needs fast iteration

---

## The Trap of One-Size-Fits-All Product Definitions

### Problem

"One product satisfies all customers" inevitably fails when requirements are diverse.

### Root Causes

- Customer use cases differ greatly
- Risk tolerance differs
- Business processes differ

### Solutions

- Provide configurable parameters and rules
- Let PMs, or future LLMs, flexibly combine signals
- Give users the right to define "what good means"

### Case Implication

LDW lane-departure warning: different customers define "departure," alert timing, and tolerance in completely different ways.

---

## Guideline Overload

### Phenomenon

Putting a 10-page guideline directly into a prompt confuses the LLM and prevents fine-grained trade-off handling.

### This Is a General Weakness of Large Models

- LLMs are not good at handling many constraints simultaneously
- Constraints may contain implicit conflicts
- Business context understanding is lacking

### Solutions

1. **Structured constraints**: Split guidelines into independent rules and apply them progressively
2. **Few-shot examples**: Replace long documents with examples
3. **Hybrid architecture**: Let the LLM handle perception and deterministic programs handle rules

---

## Multi-Agent Design Principles

### Core Insight

LLMs have inherent "personalities":
- O3: good at search and exploration, but relatively shallow analysis
- Gemini: weaker search, but deep analysis and strong synthesis

These personalities are hard to change through prompting.

### Design Implications

1. **Use complementary strengths**: Let different models do what they are good at
2. **Do not imitate human role divisions**: PM/QA/Dev are human organizational patterns and do not apply directly to agents
3. **Separate context windows**: Different agents own different subsets of context
4. **Force handoff when necessary**: When a model resists instructions, switch through code

### Current-Stage Recommendation

Hybrid systems that combine hard rules with AI capabilities are more reliable than purely agentic systems.

---

## Product Definition Before Engineering Implementation

### Core Bottleneck

For projects such as red-light running detection, the core bottleneck is the lack of a PRD, not technical capability.

### Strategy

- Turn RFC meetings into PRD discussions
- Clarify product requirements before discussing engineering details
- "What do we want" matters more than "how do we implement it"

### Causal Chain

Product form -> evaluation method -> model development strategy

The starting point is a clear product definition.

---

## Notes

- Consider regulatory differences across markets and regions
- Safety-critical systems need deterministic fallbacks
- User trust is hard to build and easy to destroy

---

## Changelog

| Date | Change |
|------|--------|
| 2026-02-22 | Initial version, integrating multiple product-design observations |
