# AI-Assisted Debugging Diagnosis

## Metadata

- **Type**: BestPractice
- **Applicable scenario**: When "the AI cannot fix the code" during AI-assisted development
- **Created**: 2026-02-21
- **Source**: Observation notes from 2026-01-19

---

## Core Insight

**In the vast majority of cases where "AI cannot fix the code," the root cause is the human user's process, not the system architecture.**

Common misunderstandings:
- "The codebase is a mess; AI cannot change it" -> actually insufficient context
- "AI is not smart enough" -> actually unclear instructions
- "We need a refactor" -> actually missing success criteria

---

## Diagnostic Decision Tree

```
AI cannot fix the code
    |
    +--> Was enough context provided?
    |       |
    |       +--> No -> Add context (relevant files, error logs, expected behavior)
    |       |
    |       +--> Yes -> Continue
    |
    +--> Were clear success criteria defined?
    |       |
    |       +--> No -> Define "what good means" (not only "it runs")
    |       |
    |       +--> Yes -> Continue
    |
    +--> Was a feedback channel provided?
    |       |
    |       +--> No -> Let AI see the result (test output, screenshots, logs)
    |       |
    |       +--> Yes -> Continue
    |
    +--> It may be a real architectural problem
            |
            +--> Consider local refactoring or splitting the problem
```

---

## Common Problems and Solutions

### 1. Insufficient Context

Symptoms:
- AI's proposed solution drifts away from the actual need
- It repeatedly edits the same piece of code
- It introduces nonexistent dependencies or functions

Solutions:
- Provide relevant files, not only the file with the error
- Provide an overview of the project structure
- Provide a similar correct implementation as a reference

### 2. Vague Success Criteria

Symptoms:
- AI asks "is this OK?" and the human says "change it more"
- After multiple rounds of edits, the human is still dissatisfied but cannot state the specific issue

Solutions:
- Define quantitative metrics (performance, coverage, error types)
- Provide examples of expected output
- Break the task into smaller verifiable steps

### 3. Missing Feedback Channel

Symptoms:
- AI cannot tell whether its edit worked
- The human has to test manually to discover problems

Solutions:
- Provide the test command and expected output
- Let AI execute the command and inspect the result
- Attach screenshots when UI is involved

---

## When It Really Is an Architectural Problem

Signals that refactoring is genuinely needed:
- The same problem appears repeatedly in different places
- The issue remains unsolved even after context is added
- Multiple AI-proposed solutions all have obvious flaws
- The problem crosses multiple module boundaries

Even then, try first:
- Local refactoring rather than a large rewrite
- Increasing test coverage
- Improving documentation and comments

---

## Relationship to Other Skills

- Use with the "70% problem" diagnosis in `bestpractice_ai_programming_mindset.md`
- Use with the verification mechanism in `bestpractice_staged_approach.md`
- Use with the Todo task-management mechanism in the system prompt for task decomposition

## Changelog

| Date | Change |
|------|--------|
| 2026-02-21 | Initial version, from observation notes dated 2026-01-19 |
