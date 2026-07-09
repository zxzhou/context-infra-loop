# Video Download and Speech Recognition Workflow

## Metadata
- Type: Workflow
- Use Case: Batch download Bilibili/YouTube videos + Whisper speech recognition
- Created: 2025-02-12
- Last Updated: 2026-03-11
- Original project archived (no longer kept in the workspace)

## Path Conventions

- Temporary downloads and intermediate artifacts: `tmp/<task_name>/`
- Final transcripts worth keeping long term: `adhoc_jobs/videos_transcribe/transcripts/`
- By default, keep only the final **plain-text transcript without timestamps**. Recommended filename: `YYYYMMDD_platform_videoid_short_slug.md`
- After the transcript is written, clean audio, `.srt`, `.vtt`, `.tsv`, `.json`, and other intermediate artifacts into the trash

## Core Flow

**Three-stage workflow:**

1. **Fetch list** -> use yt-dlp to extract video IDs (note Bilibili API limits; it may return 352 errors)
2. **Single-threaded download** -> download audio one item at a time, with 2-3 seconds between requests to avoid anti-scraping triggers
3. **Multiprocess transcription** -> run Whisper in parallel, 4-8 processes, choosing model size by hardware

## Key Decisions

| Decision Point | Choice | Reason |
|--------|------|------|
| Download concurrency | Single-threaded | Avoid triggering Bilibili anti-scraping mechanisms |
| Transcription concurrency | Multiprocess (4-8) | CPU-intensive; use multiple cores fully |
| Model choice | Depends on need | See table below |
| Output format | Keep final plain-text transcript | More stable for later search; intermediate artifacts can be reclaimed |

## Whisper Model Selection

| Model | Parameters | Speed (CPU) | Accuracy | Recommended Use |
|------|--------|-------------|--------|----------|
| tiny | 39M | 1-2 min / 10 min | Lower | Quick preview |
| base | 74M | 2-5 min / 10 min | Medium | Balanced choice |
| small | 244M | 5-10 min / 10 min | Higher | Everyday use |
| medium | 769M | 10-20 min / 10 min | High | High-quality needs |
| large-v3 | 1550M | 20-60 min / 10 min | Highest | Maximum quality |

**Performance reference**: 12 videos (3.5 hours) + large-v3 + 7 processes is about 20 minutes.

## LLM Post-Processing

Raw Whisper output usually needs post-processing:

1. **Convert to Simplified Chinese** — recognition may produce Traditional Chinese
2. **Add punctuation** — add commas, periods, and question marks based on semantics
3. **Paragraph sensibly** — split by topic and add subheadings
4. **Correct terminology** — fix specialized term recognition errors, such as mistaken biology terms
5. **Improve readability** — adjust word order and fill missing content where necessary

## Pitfall Log

| Problem | Symptom | Solution |
|------|------|----------|
| **352 error** | Request blocked by Bilibili | Add User-Agent/Referer headers, increase delay, or manually obtain IDs |
| **404 error** | Video deleted or ID incorrect | Validate ID, skip invalid videos, record failed IDs |
| **Out of memory** | Memory overflow during multiprocess transcription | Reduce parallel processes (4-6), use a smaller model, batch the work |
| **Incomplete download** | `.m4a` file cannot be played | Check file size, redownload, add integrity validation |
| **Transcription too slow** | large-v3 takes 20-60 minutes per video | Choose an appropriate model size, use GPU acceleration, chunk long videos |

## Best Practices

**Download stage:** single-threaded + 2-3 second delay + User-Agent headers + audio-only + record failed IDs.

**Transcription stage:** multiprocess (4-8) + explicit `language` parameter + skip processed files + choose model by hardware.

**Write stage:** complete download and transcription under `tmp/`, then organize the plain-text transcript and move it into `adhoc_jobs/videos_transcribe/transcripts/`.

**Cleanup stage:** after the transcript is written, delete or recycle audio, timestamped subtitles, and sidecar files. Keep only the final transcript.

**Quality optimization:** use large-v3 for key content, base/small for quick previews, and manual proofreading when needed.

**Error handling:** implement retries, validate file integrity, and handle exceptions so the script does not abort midway.
