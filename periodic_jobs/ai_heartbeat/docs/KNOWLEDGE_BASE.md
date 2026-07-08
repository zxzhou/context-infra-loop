# AI Heartbeat Knowledge Base

The AI heartbeat system maintains memory through two loops.

Loop contracts live in `periodic_jobs/ai_heartbeat/loop_specs/`. Runtime traces live in `contexts/loop_runs/ai_heartbeat/`.

## L1 Observer

The observer scans recent workspace activity, filters for useful signals, and appends observations to `contexts/memory/OBSERVATIONS.md`. It should avoid broad rewrites and should be idempotent for a given date.

Spec: `periodic_jobs/ai_heartbeat/loop_specs/heartbeat_observer.json`

## L2 Reflector

The reflector periodically reviews accumulated observations, promotes durable lessons into `rules/`, and removes stale low-value entries. Promotion requires cross-project relevance, repeated evidence, and a clear future use case.

Spec: `periodic_jobs/ai_heartbeat/loop_specs/heartbeat_reflector.json`

## Principle

Memory should be inspectable, versioned, and useful. Do not promote noise. Do not leave durable lessons trapped in transient logs.

Every loop run should end in a named terminal state. Failed or low-quality runs should be debugged from the trace, the session transcript, and the changed artifacts rather than from the final answer alone.
