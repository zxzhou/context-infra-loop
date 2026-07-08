# Setup Guide

## Purpose

This guide describes how to prepare the context infrastructure workspace on a local machine.

## Steps

1. Copy `.env.example` to `.env` and fill in the required values.
2. Install Python dependencies for the tools you plan to use.
3. Configure any external services referenced by the selected tool, such as Gmail, Kit, Typefully, Tavily, OpenAI-compatible embeddings, or OpenCode.
4. Review `docs/CRONTAB.md` before installing scheduled jobs.
5. Run individual tools manually before enabling cron.

## Verification

Use the smallest command that exercises the target path. For example, run a dry-run newsletter job before publishing, or run semantic search on a small file list before indexing a large knowledge base.
