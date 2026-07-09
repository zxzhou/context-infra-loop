# Skills Index

This index points to reusable Skills: tools, workflows, and best practices that AI can invoke.

- **Want to use a capability** -> Browse the categories below and find the corresponding skill file.
- **Want to add a new skill** -> Follow the format of the existing files and add it to the appropriate category.
- **Want to install more tool-based capabilities** -> See [`../../docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md), which lists public skill repos that can be installed separately.

---

## Component Status

### Tier 1: Core (ready after clone)
- ✅ Rules framework (SOUL/USER/COMMUNICATION/WORKSPACE) - fill in and use
- ✅ Skills framework (this directory) - fill in and use
- ✅ Three-layer memory system - requires OpenCode + cron configuration

### Tier 2: Extensions (extra configuration required)
- ⚙️ Tavily Web Search - requires a Tavily API key
- ⚙️ Semantic Search - requires LLM Studio or the OpenAI API
- ⚙️ Share Report - requires an SSH server or GitHub Pages
- ⚙️ Google Docs - requires Google OAuth
- ⚙️ Send Email - requires a Gmail App Password
- ⚙️ Delayed Execution - adapt to your own tool paths

### Tier 3: Standalone public skill repos (install as needed)
- 🔧 Image generation, Tavily, Google Docs, Outlook, Resend, OpenCode, Process Launcher, PPTX, Typefully, Stripe, and other capabilities are listed in [`docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)

### Notes
✅ = usable in at most 15 minutes
⚙️ = requires extra configuration; core functionality is unaffected if omitted
🔧 = standalone repo; install into your workspace as needed

---

## Category Index

### API Guide

Operating manuals for calling external systems or tools.

- [Practical Guide to AI CLI Agents](./ai_agent_cli_guide.md) - CLI Agent design principles, tool comparison (Claude Code / Codex / OpenCode), file-response pattern, AI calling AI
- [Tavily Web Search](./tavily.md) ⚙️ - Web search / URL extraction CLI, vendored into `adhoc_jobs/tavily_skill/`
- [Send Yourself Email Skill](./send_email.md) ⚙️ - Send email notifications through Gmail; requires an App Password
- [Share Reports to the Web](./share_report.md) ⚙️ - Convert MD reports to HTML, publish them to your own server, and return a URL
- [Google Docs Operations](./google_docs.md) ⚙️ - CLI tools: publish Markdown, create/search/modify/share documents
- [Growth Analytics](./growth_analytics.md) ⚙️ - Three CLIs for querying website traffic (GA4), email subscriptions (Kit), and Twitter interactions (Typefully)
- [Typefully Metrics CLI](./typefully_metrics.md) ⚙️ - Query Twitter impressions, engagement, and follower data through browser session credentials
- [Typefully Posting CLI](./typefully_post.md) ⚙️ - Create drafts, schedule posts, and publish tweets / threads directly through the Typefully v2 API

### Workflow

Complete workflows for specific tasks.

- [Parallel Subagent Workflow](./workflow_parallel_subagents.md) ✅ - Invoke background agents and run multiple subagents in parallel
  - **Required reading**: Read this skill before using parallel subagents for the first time
  - **No polling**: Do not repeatedly call `background_output` while agents are running; the system will notify you automatically
  - Decision criterion: the task can be split into >=2 subtasks, each requiring >=5 tool calls
  - Core parameters: parallelism <=5, research overlap 30-50%, code overlap 0-20%
- [Deep Research Workflow](./workflow_deep_research_survey.md) ✅ - Multi-agent parallelism + cross-validation (Phase 1-3 information gathering)
- [Analytical Writing Workflow](./workflow_analytical_writing.md) ✅ - Convert research material into analytical writing with judgment. Includes the Thesis Catalog (core analytical lenses L1-L6) and judgment synthesis steps. **When doing deep research and writing an external article, read both skills**
- [Cognitive Profile Extraction Workflow](./workflow_cognitive_profile_extraction.md) - Extract predictive cognitive axioms from unstructured conversation data
  - Applies to: group chats / Slack / Discord / email / podcast transcripts and any other conversation data
  - Flow: broad scan -> deep validation -> stress test -> final draft (>=3 dynamic rolling rounds)
  - **Requires the Opus model**: Opus writes the final output personally; all research is delegated + parallelized
- [AI-Generated Slide Deck Workflow](./workflow_presentation_slides.md) - Gemini rendering, Clean Ink style, 8-process parallelism, verification before 4K upscaling
- [Semantic Search Skill](./semantic_search.md) ⚙️ - Use vector similarity to retrieve deep background and evolving viewpoints
- [Knowledge Flywheel Design Pattern](./workflow_knowledge_flywheel.md) - Dumb data + dumb methods + dumb models = refined knowledge
- [Video Download and Speech Recognition Workflow](./workflow_bilibili_whisper_transcription.md) - Bilibili/YouTube video processing
- [Delayed Execution Skill](./delayed_execution.md) ⚙️ - Scheduled tasks: sleep + background execution, or OpenCode API intelligent tasks
- [Project Scaffolding and Reorganization](./project_scaffold.md) ✅ - Upgrade a loose directory into a standard project structure: `docs/`, `src/`, `scripts/`, `tests/`, `AGENTS.md`, and a standalone git repo

### BestPractice

General best practices and lessons learned.

- [Core AI Programming Methodology](./bestpractice_ai_programming_mindset.md) ✅ - the 70% problem, success criteria, verifiability
- [Skill Writing Guide (Meta-Skill)](./bestpractice_skill_writing.md) ✅ - Use when creating or rewriting skills; emphasizes result determinism, acceptance criteria, and boundary conditions
- [API Key Management and Invocation](./bestpractice_api_key_management_1password_cli.md) ✅ - Secure key management with the 1Password CLI
- [Interview Evaluation Framework](./bestpractice_interview_evaluation.md) ✅ - Trait > Skill, identifying AI-assisted cheating, probing technical depth
- [Markdown to HTML Best Practices](./bestpractice_markdown_html_conversion.md) ✅
- [PDF to Markdown](./bestpractice_pdf_to_markdown.md) ✅ - Use Docling by default; avoid MarkItDown / PyMuPDF4LLM / Marker for PDF scenarios because of quality or licensing issues
- [Time-Sensitive Information Verification](./bestpractice_temporal_info_verification.md) ✅ - Verify information that may fall beyond the knowledge cutoff
- [Staged Working Method](./bestpractice_staged_approach.md) ✅ - isolate-process-verify loop; dry run before destructive operations
- [Multi-Agent Parallel Analysis](./bestpractice_multi_agent_analysis.md) ✅ - Topic partitioning with 50% overlap and cross-validation
- [GUI Automation Methodology](./bestpractice_gui_automation.md) ✅ - Turn interfaces without APIs into programmable interfaces
- [AI-Assisted Debugging Diagnosis](./bestpractice_ai_debugging_diagnosis.md) ✅ - Root-cause decision tree for "AI cannot fix the code"
- [AI Product Design Principles](./bestpractice_ai_product_design.md) ✅ - Linear chat vs knowledge work, decoupling perception and rules
- [Reverse Engineering Product/Technical Decisions](./bestpractice_product_decision_analysis.md) ✅ - Analyze product or technical decisions through design space, constraints, and trade-offs

---

## How to Add Your Own Skill

Before creating or rewriting a skill, first read [`bestpractice_skill_writing.md`](./bestpractice_skill_writing.md). It explains how to define a skill through goals, acceptance criteria, available resources, and output specifications instead of writing it as a mechanical step checklist.

Recommended file naming: `<category>_<name>.md`, such as `workflow_my_process.md` or `bestpractice_my_insight.md`. After writing it, add an entry under the corresponding category in this INDEX so future agents can find it.

## Progressive Disclosure

Skills use progressive disclosure:
- **INDEX.md** provides an overview for quick navigation
- **Specific skill files** contain complete operating steps and examples
