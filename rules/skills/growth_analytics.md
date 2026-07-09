---
title: Growth Data Analytics Toolkit
category: API Guide
tags: [analytics, ga4, kit, typefully, growth, metrics]
created: 2026-03-14
updated: 2026-03-14
---

# Skill: Growth Analytics (GA4 / Kit / Typefully)

Three CLI tools for querying website traffic (GA4), email subscriptions (Kit), and Twitter publishing and engagement data (Typefully).

## When to Use

Trigger this skill when the user expresses intents such as:
- "Check recent traffic" or "How is the website data?"
- "How much did subscribers grow?" or "What is the open rate?"
- "Twitter engagement data" or "How many impressions?"
- "Do a growth analysis" or "Pull growth data"
- Any query involving the <your-site> website, Newsletter, or social media metrics

## Prerequisites

- Root `.env` contains:
  - `KIT_API_KEY` - Kit (ConvertKit) API v4 key
  - `TYPEFULLY_API_KEY` - Typefully v2 API key (for publishing queries)
  - `GA4_CREDENTIALS_PATH` - absolute path to the GA4 service account JSON file
- Typefully browser-level credentials (optional, only needed for engagement metrics):
  - `TYPEFULLY_AUTHORIZATION`, `TYPEFULLY_ACCOUNT`, `TYPEFULLY_SESSION`
- Python venv is activated (`source .venv/bin/activate`)

## Tool 1: Kit Subscription Data

```bash
python tools/kit_metrics.py account              # account information
python tools/kit_metrics.py growth               # subscription growth over the last 14 days
python tools/kit_metrics.py growth --start-date 2026-02-28 --end-date 2026-03-14
python tools/kit_metrics.py email-stats           # open rate / click rate over the last 90 days
python tools/kit_metrics.py subscribers --count   # current active subscriber count
python tools/kit_metrics.py broadcasts --limit 10 # latest 10 emails
python tools/kit_metrics.py broadcast-stats 23288438  # single email open rate / click rate
python tools/kit_metrics.py snapshot              # full data snapshot
python tools/kit_metrics.py snapshot --output /tmp/kit_snapshot.json
```

### Key Kit Metrics

- **growth_stats**: new subscriptions, unsubscribes, net growth, and total count within a period
- **email_stats**: 90-day aggregate sends, opens, and clicks
- **broadcast stats**: single-issue open_rate, click_rate, unsubscribes
- **subscribers**: active/inactive/unsubscribed subscriber lists and totals

## Tool 2: GA4 Website Traffic

```bash
python tools/ga4_metrics.py daily --days 7        # daily traffic trend
python tools/ga4_metrics.py weekly --days 90       # weekly aggregate
python tools/ga4_metrics.py top-pages --limit 20   # top pages
python tools/ga4_metrics.py sources                # traffic source details
python tools/ga4_metrics.py channels               # channel grouping
python tools/ga4_metrics.py campaigns --days 14    # UTM campaign attribution (Twitter effect tracking)
python tools/ga4_metrics.py snapshot --output /tmp/ga4_snapshot.json  # full snapshot
```

### Key GA4 Metrics

- **daily/weekly**: activeUsers, newUsers, sessions, screenPageViews, averageSessionDuration, bounceRate
- **top-pages**: pagePath, pageTitle, screenPageViews, activeUsers
- **sources**: traffic distribution by sessionSource and sessionMedium dimensions
- **channels**: sessionDefaultChannelGroup (Direct, Organic Search, Referral, Social, etc.)
- **campaigns**: sessionCampaignName - used to verify whether UTM-tagged Twitter threads and similar campaigns actually brought traffic

### GA4 Property

- Property ID: *(obtained from the GA4 console)*
- Website: <your-site> (Computing Life)
- Service Account JSON location: specified by `GA4_CREDENTIALS_PATH` in `.env`

## Tool 3: Typefully Twitter Data

### Publishing Data (v2 API, API Key Auth)

```bash
# View published tweets/threads
curl -s -H "Authorization: Bearer $TYPEFULLY_API_KEY" \
  "https://api.typefully.com/v2/social-sets/<your-social-set-id>/drafts?status=published&limit=50"
```

Social set ID: *(obtained from the Typefully API)*

### Engagement Data (Browser Session Auth)

```bash
python tools/typefully_metrics.py snapshot         # full engagement snapshot
python tools/typefully_metrics.py metric impressions --start-date 2026-03-01
python tools/typefully_metrics.py metric engagements
python tools/typefully_metrics.py metric followers
```

See `rules/skills/typefully_metrics.md` for details.

**Note**: The Typefully engagement API requires browser-level credentials (TYPEFULLY_AUTHORIZATION / ACCOUNT / SESSION), which must be captured from the Typefully web app. The v2 API key can only query publishing status; it cannot query impressions/engagement.

## Typical Usage

### Quick Growth Overview

```bash
# One command for full Kit data
python tools/kit_metrics.py snapshot

# One command for full GA4 data
python tools/ga4_metrics.py snapshot
```

### Verify Twitter Promotion Effect

```bash
# Query GA4 UTM campaign data to see whether a Twitter thread brought traffic
python tools/ga4_metrics.py campaigns --days 14
```

### Cross-Analysis

Pull Kit and GA4 data together to compare subscription growth and traffic trends:

```bash
python tools/kit_metrics.py growth --start-date 2026-03-01 --end-date 2026-03-14
python tools/ga4_metrics.py weekly --days 30
```

## Data Storage

To persist historical data, save JSON with the `--output` parameter. Historical data and reports for growth analysis projects live in `adhoc_jobs/website_growth/`.

## Notes

- Kit API rate limit: 120 requests / 60 seconds
- GA4 Data API has quota limits. The `snapshot` command runs multiple reports at once, so avoid calling it too frequently
- The Typefully engagement API is a private API and may change at any time
- All tools output JSON to stdout by default; format with `| python3 -m json.tool`
