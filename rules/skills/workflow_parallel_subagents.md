# Parallel Subagent Workflow

## Metadata

- **Type**: Workflow
- **Use Case**: Calling background agents and running multiple independent subtasks in parallel
- **Created**: 2026-02-20
- **Last Updated**: 2026-03-01

---

## When to Use Parallel Mode

Parallel execution is worthwhile only when all of the following are true:

1. **The task is decomposable**: it can be split into at least 2 relatively independent subtasks
2. **The subtasks have enough scale**: each subtask is expected to need at least 5 tool calls
3. **The subtasks have value**: parallel execution saves significant time compared with serial execution

If these conditions are not met, execute serially. Do not parallelize for its own sake.

---

## Parallel Execution Flow

### 1. Evaluate and Split

After identifying 3-5 key dimensions, choose the overlap according to task type:

| Task Type | Overlap Range | Reason |
|---------|-------------|------|
| Research / creative tasks | 30% - 50% | Cross-checking and gap-finding |
| Code / execution tasks | 0% - 20% | Prioritize efficiency and reduce duplication |

### 2. Start in Parallel

Issue all calls in the same message. Use `mcp_task()` and choose `category` or `subagent_type` according to task type:

```python
# Research / analysis tasks -> use subagent_type
mcp_task(
    subagent_type="explore",
    run_in_background=True,
    prompt="Specific dimension description..."
)

# Implementation tasks -> delegate by category
mcp_task(
    category="deep",
    load_skills=["git-master"],
    run_in_background=True,
    prompt="Specific implementation requirements..."
)
```

Each subagent prompt should include:
- The specific dimension/scope it owns
- The expected overlap area (so the agent knows others are also looking there)
- Output format requirements

### 3. Wait and Integrate

After launching, do nothing and wait for the system notification. The system automatically pushes a `<system-reminder>` notification when a subagent finishes. After receiving it, use `mcp_background_output(task_id="...")` to retrieve the result, then cross-check overlapping areas and synthesize the final output.

**Common misunderstanding about `background_output`:**

The `block` and `timeout` parameters of `background_output` **do not** make the call block until the task is complete. Whether you set `timeout=120` or `timeout=600`, it **immediately returns whatever output is currently available**. This means:

- **Wrong**: repeatedly calling `background_output(block=true, timeout=600)` trying to "wait" for completion; each call immediately returns the same partial result and creates meaningless polling.
- **Right**: after launching the background task, **end your response**, wait for the system-pushed `<system-reminder>` notification, then call `background_output` once to retrieve the complete result.

In short: `background_output` is a tool for **retrieving results**, not **waiting for results**. Waiting is handled by the system notification mechanism.

---

## Examples

### Research Task (30-50% overlap)

```
Research "adoption of a technical framework"
├─ Agent 1 (explore): core features + community activity
├─ Agent 2 (librarian): community activity + enterprise cases
├─ Agent 3 (oracle): enterprise cases + competitor comparison
└─ Overlap: community and enterprise cases are both covered for cross-checking
```

### Code Task (0-20% overlap)

```
Implement "user authentication system"
├─ Task 1: authentication core logic + token management
├─ Task 2: database models + migration scripts
├─ Task 3: API endpoints + test cases
└─ Overlap: small amount around interface definitions to ensure integration correctness
```

---

## Notes

- **Do not over-parallelize**: 2-3 carefully designed subagents are usually better than 5 loose ones.
- **Prompt quality**: subagent prompts must be specific enough; otherwise results will be shallow.
- **Cost awareness**: parallelism consumes more tokens, so evaluate whether it is worth it.
- **Intermediate results**: usually do not need to be saved; integrate them in the main agent.
