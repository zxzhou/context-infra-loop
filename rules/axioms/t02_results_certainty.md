---
id: axiom_results_certainty_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T2. Results Certainty Over Process Certainty

## 1. Core Axiom

Define what counts as `correct` and verify it first; do not try to make AI reliable by micromanaging every step.

## 2. Deep Reasoning

### 2.1 The Ceiling of Process Certainty

In traditional programming, confidence comes from process certainty: every line of code is under your control, and every branch and edge case has been designed by you. This certainty is tangible, and it is the core capability we have trained for years: translating outcomes into program behavior. But this pattern runs into a fundamental dilemma in AI systems.

When you try to constrain AI behavior with rules, you find yourself trapped in an infinite loop of defensive programming. One rule fixes one problem but introduces new problems in other situations. You add more rules to handle edge cases, but edge cases are infinite. Eventually, you discover that you are maintaining more rules than product logic. This is exactly the dilemma I encountered in an AI translation project: chunking, retries, glossaries, resumable checkpoints, Chinese character detection, timeout handling -- each existed to prevent a specific failure mode. But these defensive rules themselves became the main source of system complexity, and they could never cover every situation.

The ceiling of process certainty depends on how many edge cases you can imagine. In AI systems, edge cases are infinite because AI behavior is fundamentally nondeterministic. You can never fully constrain it with rules.

### 2.2 The Results-Certainty Loop

Results certainty represents a completely different way of thinking: instead of specifying the process, define a clear target state and let the system find its own way there. The key is to establish a loop: execute -> observe -> verify -> correct.

When I handed the translation task to Claude Code, this loop became genuinely possible. Claude Code's basic unit of operation is the file, and files are stateful and persistent. This means the AI can see what it has already done, run verification scripts to check the result, and adjust based on feedback. This is not a one-off API call, but an iterative, self-correcting process.

Concretely, when I define the standard for "translation complete" -- correct formatting, no remaining Chinese characters, consistent terminology -- I can encode those standards as executable checks. The AI not only completes the translation, but also runs those checks, sees the failure messages, and fixes the problems itself. This process can repeat until every check passes. The key shift is that I no longer need to foresee every possible failure mode; I only need to define what success means.

This principle also has deep implications for cost structure. In traditional programming, code execution is nearly free while human labor is expensive, so we invest heavily in designing perfect logic. But in the AI era, inference costs are falling quickly. Multiple attempts, checks, and corrections are often cheaper than writing defensive rules for every long-tail failure mode. This is a fundamental economic shift.

### 2.3 Making Acceptance Criteria Explicit

Results certainty depends on being able to define "done" clearly. This sounds simple, but it is actually the biggest bottleneck. Most failures do not happen because the AI is not smart enough; they happen because the AI does not know what "done" means.

I use an analogy to understand this problem: imagine assigning a task to an intern with amnesia. This intern has no background knowledge, does not know what you discussed before, and does not know your implicit expectations. They can only see the instructions you gave this time. If you want them to complete the task reliably, you must write the acceptance criteria with extreme clarity -- clear enough that they can judge from those criteria whether they are done. If they think they are not done, they know what is missing.

This is exactly how Claude Code works. When I say "translate this file, then run this Python script to check for remaining Chinese characters, and fix them if any remain," I am turning implicit expectations into explicit, verifiable standards. That shift itself is the biggest lever.

### 2.4 Architecture Over Rules

When a system performs poorly, our first reaction is often "the model is not good enough" or "we need more rules." In reality, many failures come from poor architecture. The Wide Research example is instructive: rather than asking a single AI call to execute a complex task perfectly, split the task into multiple small steps, each with clear acceptance criteria. This is not model magic; it is management repair.

The same principle applies to translation. When an API call "slacked off" on long text, I once thought it was a model problem. In reality, it was an architecture problem: long output reduces instruction following. The solution is not to ask the model to be "smarter," but to change the architecture -- have the AI translate chapter by chapter, with clear input and output for each chapter, and make each chapter independently verifiable. Then the problem changes from "how do we make one API call execute perfectly" to "how do we design a workflow where each small step is reliable."

## 3. Application Criteria

### When to Use

Results certainty applies to any task whose output can be checked. This includes:

- **Formatting tasks**: code generation, document conversion, data cleaning -- all have clear success criteria.
- **Verification tasks**: checking whether specific conditions are met (no remaining Chinese, tests pass, conforms to a spec).
- **When guardrail rules start outnumbering product logic**: this is a signal that you should shift toward results certainty.

### How to Practice

1. **Write acceptance criteria first**: Do not say "generate high-quality code." Say "the code must pass all unit tests, coverage must be > 80%, and there must be no security warnings." Turn implicit expectations into explicit, measurable standards.

2. **Turn standards into executable checks whenever possible**: Python scripts, unit tests, linters, regular expressions -- anything that can automatically verify should be automated. Then the AI can run checks itself, see failures, and fix them.

3. **Let the agent choose methods and iterate**: Do not specify how the AI must do the work; define what success means. The AI may use regex checks, NLP, or another method. If the final result satisfies the standard, it is reliable.

4. **Build a feedback loop**: Ensure the AI can see verification results and adjust based on failure information. This loop is the core of results certainty.

## 4. Traps and Boundaries

### When It Does Not Apply

- **Acceptance criteria cannot be defined**: If success is inherently subjective (such as "creative writing"), results certainty is difficult.
- **Extremely high real-time requirements**: If verification creates unacceptable latency, you may need to accept higher risk.
- **Cost-benefit mismatch**: If verification costs far more than failure, the investment may not be worth it.

### Common Traps

1. **Fake acceptance criteria**: Defining standards that look clear but are actually vague. For example, "good code quality" is not a standard; "passes all tests and complexity < 10" is.

2. **Verification blindness**: The verification rule itself is flawed, so outputs that pass verification still fail. Verification rules need regular review to ensure they are measuring what you actually care about.

3. **Over-verification**: Designing an overly complex verification process for low-risk tasks, reducing efficiency. Verification should match the risk level.

4. **Trust drift**: Over time, verification standards gradually loosen until the system becomes unreliable. Regular review and recalibration are required.

## 5. Relationship to Other Axioms

- **A04 Reliability Is a Management Problem**: Results certainty is the core method of reliability management.
- **V02 Verifiability Is the Foundation of Trust**: Results certainty depends on clear acceptance criteria and executable checks.
- **T07 Isolation-Processing-Verification Loop**: Results certainty is the verification phase of this loop.
- **T01 Infrastructure Over Components**: Results certainty needs a runtime that supports feedback loops, such as Claude Code.
