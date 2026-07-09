# Public Skill Ecosystem

The `rules/skills/` directory shipped with `context-infrastructure` is a starter set. It shows how skills should be organized, indexed, and invoked. More complete capabilities should not all be copied into this repository; they should be installed through independent public skill repositories. This has two benefits. First, each skill repo can keep its own README, CLI, tests, and release cadence. Second, private aliases, paths, tokens, and business context in the user's workspace can stay in a local overlay instead of leaking into the public repo.

This page is for both humans and AI agents. Humans can use it to discover additional installable capabilities. AI agents can follow the installation protocol here to connect a public skill repo to the target workspace.

## Installation Protocol

Give the following text, together with the target repo URL, to your coding agent:

```text
Install this public skill repo into my workspace:
<GitHub URL>

Start from my workspace AGENTS.md or CLAUDE.md. Follow any WORKSPACE.md or skills/INDEX.md routing rules. Clone or vendor the repo under an appropriate project directory. Expose exactly one root skill to my global skill index or agent instructions. Keep private aliases, local paths, credentials, endpoint defaults, and business context in a local overlay, not in the public repo.
```

After installation, the workspace usually has two layers: the public repo owns the generic technical contract, while local `rules/skills/` files or `.env` own private configuration. For example, the iMessage public repo only provides a send-only CLI; the local overlay stores contact aliases. The Stripe public repo only provides a read-only analytics contract; the local overlay stores concrete business attribution.

## Recommended Public Skill Repos

| Area | Repo | Capability |
|---|---|---|
| Web search | [tavily-skill](https://github.com/grapeot/tavily-skill) | Tavily search/extract CLI with stable JSON output for agents |
| Documents | [gdocs-skill](https://github.com/grapeot/gdocs-skill) | Google Docs creation, search, editing, sharing, Markdown, and tabs |
| Email | [outlook_skill](https://github.com/grapeot/outlook_skill) | Outlook.com email download, archiving, Markdown rendering, sending, and calendar invites |
| Email | [resend_email_skill](https://github.com/grapeot/resend_email_skill) | Resend custom-domain sending, inbox reading, Markdown export, and attachment checks |
| Messaging | [imessage_skill](https://github.com/grapeot/imessage_skill) | macOS iMessage send-only CLI; contact aliases live in the local overlay |
| Agent operations | [opencode_skill](https://github.com/grapeot/opencode_skill) | OpenCode job submission, batch tasks, SQLite data maintenance, and archive operations |
| Agent operations | [process-launcher](https://github.com/grapeot/process-launcher) | Local HTTP process launcher, useful for TCC / GUI permission bridging |
| Usage analytics | [ai_usage_dashboard](https://github.com/grapeot/ai_usage_dashboard) | Multi-platform AI token usage, cost estimation, local dashboard, and E1002 JSON |
| Social / growth | [typefully-twitter-skill](https://github.com/grapeot/typefully-twitter-skill) | Typefully posting, account metrics, and X/Twitter per-post analytics |
| Payments / growth | [stripe-skill](https://github.com/grapeot/stripe-skill) | Stripe read-only finance / sales analytics; live tests are opt-in by default |
| Media | [online-media-skill](https://github.com/grapeot/online-media-skill) | Online media download, ASR artifacts, query packs, and source-identification workflows |
| Slides | [pptx.skill](https://github.com/grapeot/pptx.skill) | AI-first PPTX reading, editing, and rendering |
| Images | [image-generation-skill](https://github.com/grapeot/image-generation-skill) | Gemini Flash / Gemini Pro / GPT-Image-2 text-to-image, image editing, and upscaling |
| Images | [tiff-icc-profile](https://github.com/grapeot/tiff-icc-profile) | Embed ICC profiles into untagged TIFF files, commonly used in DaVinci still workflows |
| Health | [health-quantification](https://github.com/grapeot/health-quantification) | Apple Health / manual records -> SQLite -> CLI -> AI analysis |
| Coffee | [roest-analysis](https://github.com/grapeot/roest-analysis) | Roest roast-log capture and analysis |
| Intake | [intake-skill](https://github.com/grapeot/intake-skill) | Public-ready skill for voice memos and intake workflows |

## Selection Principles

If a capability needs a complete CLI, tests, fixtures, or long-term maintenance, make it an independent repo. `context-infrastructure` should link to it, not copy it. This lets users install capabilities as needed without turning the starter workspace into a giant tool bundle.

If a capability is a general working method, such as deep research, parallel subagents, analytical writing, skill writing, or project scaffolding, it can stay in this repository's `rules/skills/`. Those files are the core reference implementation and should be readable and adaptable immediately after clone.

If a capability depends on private data, private accounts, or business context, put the generic part in the public repo and keep the private part in the user's own workspace overlay. Do not write real contacts, servers, paths, API keys, customer names, transaction data, or usage records into the public repo.
