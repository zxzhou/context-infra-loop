# AI Heartbeat PRD

## Goal

Create a lightweight memory maintenance loop for the context infrastructure repository.

## Users

The primary users are the human owner and AI agents working in the repository.

## Requirements

- Append daily observations without duplicating dates.
- Separate high, medium, and low priority memory.
- Promote reusable lessons into the correct rule files.
- Preserve source paths so future agents can trace context.
- Keep scheduled jobs auditable and easy to disable.

## Non-Goals

- Replacing human judgment.
- Turning every task log into permanent memory.
- Creating a complex database when files and Git history are sufficient.
