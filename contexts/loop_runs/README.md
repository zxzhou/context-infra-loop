# Loop Run Traces

This directory stores compact run traces for agent loops.

Each trace should make a run auditable without copying the full prompt or raw tool output. A trace records the loop name, spec path, prompt hash, inputs, session ID, model, expected artifacts, timestamps, terminal state, and any startup error.

Use these traces for:

- debugging failed or stalled agent runs
- identifying repeated harness failure modes
- selecting past runs for replay or evals
- separating loop behavior from one-off chat history

Do not store secrets, full model transcripts, or bulky generated artifacts here.
