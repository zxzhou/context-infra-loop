---
id: axiom_first_principles_methodology_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T8. First-Principles Methodology Design

## 1. Core Axiom

Before adopting any framework, restate the problem from first principles (uncertainty, constraints, success criteria), and borrow only the parts that directly serve it. A methodology is not a fixed set of rituals; it is a product designed for a specific user, a specific task, and specific failure modes.

## 2. Deep Reasoning

### 2.1 The Hidden Cost of Frameworks: Worldview Lock-in

A complete framework is often a form of worldview lock-in. It quietly inserts assumptions about roles, stages, and artifacts that may not match your domain. When you choose a framework, you are not merely choosing a set of tools; you are choosing the framework author's understanding of "the right way to solve problems." This is especially dangerous when the domain foundation has not yet settled. Agentic AI is still evolving quickly, and any medium-to-high abstraction is inherently fragile. AutoGen's shift from v0.3 to v0.4 was essentially a full rewrite, showing that even mature frameworks can face fundamental rethinking. Locking in too early creates technical debt and limits your ability to understand the domain fully. When you are constrained by a framework's abstractions, you cannot see the real mechanisms underneath; when new understanding appears, you have already invested too much to pivot easily.

### 2.2 The Mismatch Between Human Organizations and AI Systems

Methods built to coordinate humans (rituals, role granularity, process certainty) can backfire when the bottleneck is AI reliability or scientific uncertainty. BMAD-METHOD is instructive: it rigidly copies human professional specialization (Analyst, PM, Architect, Scrum Master, Developer, QA) into the AI world. But the assumption itself deserves questioning. Human society has professional specialization because we are limited: one person cannot simultaneously master product, design, engineering, and testing within a decade or so of education. LLMs are different. A sufficiently strong model can itself understand business, design architecture, write code, and test. When you give it a prompt saying "you are a senior software engineer," you are actually limiting it rather than enhancing it. You are lowering an omnipotent-seeming LLM to the level of a weak human who can wear only one hat.

The real value of multi-agent systems should come from context isolation, not role-play. Boundaries between agents should be drawn according to the coupling of the task itself, not according to professional divisions in human society. The division between a planning agent and an execution agent exists because planning and execution require completely different contexts, not because "PM and Developer are different jobs in human society."

### 2.3 Methodology as Product Design

I treat methodology as a product: it needs a user (me/the team), a job to be done, and measurable failure modes. This perspective changes everything. Instead of asking "does this framework look disciplined," ask "can this methodology help me solve my specific problem?" In the retrospective on the FCW/TTC debate, reverse-engineered project management collided with modeling uncertainty; this taught me to choose methods by uncertainty range rather than by whether they look "disciplined."

When uncertainty is high (for example, exploratory research or the early stage of a new domain), heavy process becomes a burden. You need fast feedback loops, flexible iteration, and minimal documentation. When uncertainty is low (for example, known engineering tasks with clear requirements), structured process has value: it ensures details are not missed and detours are avoided. If the same methodology claims to fit both situations, it has not truly understood the nature of the problem.

### 2.4 The Cost of Heavy Process: Overkill for Lightweight Tasks

BMAD's standard flow is: market research -> project brief -> PRD -> architecture document -> user stories -> development loop -> acceptance and release. This flow is reasonable for medium-to-large projects that require long-term maintenance. The problem is that not all software development needs this flow. The AI era has produced a large amount of "user-generated software" -- software that may serve only one person, be used only once, and be thrown away afterward. Examples include a script that checks daily whether a site has new updates, or renaming thirty videos according to a rule. For tasks like these, forcing them through PRD -> architecture -> user stories is using a sledgehammer on a tiny problem.

The more fundamental issue is that BMAD treats agile process as a fixed template rather than a set of principles that should be adapted to local conditions. True agility is about quickly responding to change. BMAD's design, to some degree, replaces flexibility of judgment with certainty of process. That is valuable in some scenarios, but you must be clear about its cost.

### 2.5 Composability and Exit Ramps

The best methodologies are composable: they preserve exit ramps (what do we stop doing when cost exceeds benefit?). This means every part of the methodology should be optional and replaceable rather than one tightly coupled whole. If you find that a step (such as a detailed architecture document) does not help your project, you should be able to skip it directly instead of being forced to follow the whole process.

The benefit of this design is that it allows you to adjust according to reality. You can start with a lightweight version, then add more structure gradually as project complexity increases. When project complexity decreases, you can also simplify the process. This flexibility is key to surviving in a fast-changing environment.

## 3. Application Criteria

### When to Use

Apply first-principles methodology design when evaluating popular AI development frameworks (such as agent role-play workflows), choosing research versus engineering cadence, and standardizing team practices. Specific scenarios include:

- **Framework choice**: Before adopting frameworks such as BMAD, LangGraph, or AutoGen, first ask: what are this framework's core assumptions? Do those assumptions match my problem? If they do not match, should I change the problem to fit the framework, or reject the framework?
- **Process design**: When designing a workflow for a team or project, do not directly copy industry best practices. Start from your specific constraints. What is your main uncertainty? What are your failure modes? What process can most effectively address those challenges?
- **Tool selection**: When choosing development tools, frameworks, or methodologies, evaluate whether they truly solve your core problem rather than being misled by marketing.

### How to Practice

**Step 1: Make Assumptions Explicit**

Write down the framework or methodology's core assumptions. For example, BMAD's assumptions include:
- Software development needs clear stage separation.
- Different roles should have different responsibilities and contexts.
- Documentation is an important project deliverable.
- Process certainty can improve quality.

**Step 2: Map to Constraints**

Map each assumption to your specific constraints. Does your project truly need this kind of stage separation? Does your team truly need this role division? Is your uncertainty low enough for process certainty to create value?

**Step 3: Small-Scale Pilot**

Run a small-scale pilot with explicit success metrics. Do not adopt everything at once; test the methodology within a limited scope. Metrics should answer: did this methodology actually help us complete the task faster? Did it reduce errors? Did it improve code quality?

**Step 4: Keep Templates, Discard Rituals**

If the pilot succeeds, keep the parts that genuinely have value (such as PRD templates or architecture document structure), but discard pure rituals (such as daily standups or lengthy review processes). The value of a methodology lies in its artifacts and way of thinking, not in its rituals.

**Step 5: Iterate Continuously**

Review your methodology regularly. Every three months, ask: is this methodology still effective? Have new constraints or failure modes appeared? Does it need adjustment? Methodology is not fixed; it should evolve as your understanding of the problem evolves.

## 4. Traps and Insights

### 4.1 The "Framework Worship" Trap

Many people say "we adopted BMAD" or "we use Scrum," as if choosing a framework solves every problem. In reality, a framework is a reference, not scripture. Tools become outdated; understanding the essence of tools does not. What is worth learning from BMAD is its engineering thinking about agile process, not framework worship. Treat it as a reference, not a rule that must be obeyed.

### 4.2 The "One-Size-Fits-All" Trap

If the same methodology fits every project, it has not truly understood the nature of the problem. A good methodology should be adjustable according to specific circumstances. If you find yourself forcing your problem to fit a methodology rather than the methodology adapting to your problem, it is time to reassess.

### 4.3 The "Cost-Benefit Imbalance" Trap

Many teams invest substantial time and energy following a methodology but never ask whether that investment actually produced value. When cost exceeds benefit, you should have the courage to abandon the methodology instead of continuing to insist on it. This is why "exit ramps" matter: they give you an elegant way to quit.

## 5. Related Axioms

- **A06. Framework Choice Is Worldview Lock-in** -- The purpose of first-principles methodology design is to help you make conscious decisions when choosing frameworks rather than passively accepting a framework author's worldview.
- **A07. Design Philosophy Determines the Ceiling of Capability** -- Different methodologies embody different design philosophies. Understanding those philosophical differences helps you choose the methodology that fits you best.
- **T01. Infrastructure Over Components** -- The value of a methodology lies in its infrastructure (document structure, context management, observability), not its components (tools, frameworks, processes).
- **T02. Results Certainty** -- The ultimate goal of first-principles methodology design is to ensure you can reliably achieve the expected results.

## 6. Summary

The core idea of first-principles methodology design is simple: do not blindly adopt frameworks. Start from your specific problem and design a methodology tailored to it. This process includes making assumptions explicit, mapping them to constraints, piloting at small scale, keeping valuable parts, and iterating continuously.

In the AI era, this principle matters even more because AI capability boundaries are still changing rapidly, and any framework's assumptions may soon become outdated. The wisest approach is to stay framework-neutral, start from first principles, use libraries rather than frameworks, and embrace a builder mindset. The cost is low (because the base system is simple), but the payoff is high (because you preserve complete flexibility and depth of understanding).

Finally, remember: methodologies serve people, not the other way around. When a methodology becomes a burden, it is time to reassess.
