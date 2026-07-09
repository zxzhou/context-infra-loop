# Skill: Typefully Posting CLI

Create drafts, schedule posts, publish immediately, and post tweets or threads through the Typefully v2 API.

## When to Use

Trigger this skill when the user expresses intents such as:
- Post a tweet
- Post to Twitter / post to X
- Put this article on Twitter
- Schedule a tweet
- After publishing the shared report, post it to Twitter too

## Prerequisites

- The root `.env` contains:
  - `TYPEFULLY_API_KEY`: Typefully API key
  - `TYPEFULLY_SOCIAL_SET_ID`: the social set ID for the target account
- Python venv is activated
- Dependencies are installed: `pip install -r tools/requirements.txt`

Typefully API keys can be generated in Settings -> API. The social set ID must be obtained from your own Typefully account configuration.

## Five Publishing Rules

1. **Default to a single post, not a thread**: Only publish a thread when the content naturally needs to be split into 2-4 posts, or when the user explicitly asks for a thread.
2. **Prefer scheduling when a URL is included**: This workflow defaults to scheduling URL-bearing tweets 1-2 minutes later instead of publishing with `now`. This is more stable and leaves room for a final copy and link check.
3. **Use UTM on URLs**: Links should use tracked URLs, for example `https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch-post`.
4. **Validate length with weighted count**: Run `count` before publishing; do not eyeball the 280-character limit. URLs count as 23, and CJK characters usually count as 2.
5. **Enable long posts explicitly**: When content exceeds the standard tweet length, use `--long-post`. Long posts and threads are different formats; do not mix them.

## Usage

Run all commands from the repo root.

### Single Tweet

```bash
python tools/typefully_post.py draft --text "Hello from the API!"
python tools/typefully_post.py post --text "Going live now!" --publish-at now
python tools/typefully_post.py post --text "Tomorrow morning" --publish-at "2026-04-20T16:00:00Z"
python tools/typefully_post.py count --text "Draft tweet with URL https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch-post"
```

### Long Post

```bash
python tools/typefully_post.py post --text "$(cat long_post.md)" --publish-at "2026-04-20T16:00:00Z" --long-post
```

### Thread

Thread file format: separate each tweet with `---`.

```bash
python tools/typefully_post.py post --thread-file my_thread.md
python tools/typefully_post.py schedule 12345 --at "2026-04-20T16:00:00Z"
printf "First tweet\n---\nSecond tweet" | python tools/typefully_post.py post --thread-stdin
```

### Draft Management

```bash
python tools/typefully_post.py list --status published --limit 10
python tools/typefully_post.py list --status draft
python tools/typefully_post.py get 12345
python tools/typefully_post.py publish 12345
python tools/typefully_post.py schedule 12345 --at "2026-04-20T16:00:00Z"
python tools/typefully_post.py schedule 12345 --next-free-slot
python tools/typefully_post.py delete 12345
python tools/typefully_post.py draft --text "tweet content" --draft-title "Launch post"
```

## Pre-Post Checks

First run the local CLI weighted count:

```bash
python tools/typefully_post.py count --text "your copy https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch-post"
python tools/typefully_post.py count --thread-file my_thread.md
```

The output shows each tweet's `weighted_length/280`; over-limit posts are marked `TOO_LONG`.

## Writing Habits

- Observation first: start with an observation, number, or choice that changes the reader's judgment, then give the conclusion.
- One tweet should carry one main judgment; treat the link as further reading.
- Default to one URL. Put it at the end for a single tweet, and in the last tweet for a thread.
- The style should lean engineer-like: less summary voice, more judgment and observation.

## Optional Workflow

If you already have your own sharing workflow, attach this skill after it:

1. Publish the article or report and get the public URL.
2. Add UTM parameters to the URL.
3. Write the tweet copy and run `count` first.
4. Finally send it with `post` or `draft + schedule`.

## Notes

- `--publish-at` supports `now`, `next-free-slot`, or an ISO timestamp.
- `post --thread-file` is suitable for creating a thread draft first; if you need precise timing, `draft` followed by `schedule` is more direct.
- `TYPEFULLY_API_KEY` and `TYPEFULLY_SOCIAL_SET_ID` should both be provided by the user. Do not write them into the repo.
