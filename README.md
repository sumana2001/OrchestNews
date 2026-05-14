# OrchestNews 🚀

**AI-Powered Weekly Technology Intelligence Pipeline using Kestra + Ollama + Notion + Slack**

---

# Overview

OrchestNews is a fully local, zero-cost workflow orchestration project built using Kestra that automatically generates a weekly AI & technology news digest.

The system fetches trending AI/tech news from RSS feeds, filters duplicate articles, summarizes them using a local LLM running via Ollama, extracts macro-level industry insights, ranks articles using lightweight personalization logic, stores everything in Notion, and finally sends a digest notification through Slack.

The project demonstrates:

- Workflow orchestration
- AI-powered summarization
- Local LLM inference
- Multi-system integrations
- Data transformation pipelines
- Scheduling and automation
- Fault tolerance & defensive engineering

---

# High-Level Architecture

```text
RSS Feeds
   ↓
Fetch News
   ↓
Deduplicate Articles
   ↓
LLM Summarization (Ollama)
   ↓
Article Ranking + Personalization
   ↓
Trend Extraction (LLM)
   ↓
Upload to Notion
   ↓
Slack Notification
```

---

# Tech Stack

| Component              | Technology     |
| ---------------------- | -------------- |
| Workflow Orchestration | Kestra         |
| LLM Runtime            | Ollama         |
| Model Used             | `phi3`         |
| Storage                | JSON + Notion  |
| Notifications          | Slack          |
| Language               | Python         |
| Deployment             | Local + Docker |
| News Sources           | RSS feeds      |

---

# Key Features

## ✅ Automated Weekly AI Digest

Runs automatically every Sunday morning using a cron-based Kestra trigger.

---

## ✅ Multi-Source News Aggregation

Fetches articles from:

- TechCrunch AI
- Hacker News
- MIT Technology Review

using RSS feeds.

---

## ✅ Duplicate/Noise Filtering

Uses fuzzy title matching to:

- remove duplicate stories
- reduce repetitive news
- prioritize unique insights

---

## ✅ Local AI Summarization

Uses local LLM inference via Ollama (`phi3`) to:

- summarize articles
- classify article categories
- assign importance scores

No paid APIs are used.

---

## ✅ AI Trend Extraction

Combines article summaries and extracts:

- macro technology trends
- emerging themes
- ecosystem patterns

Examples:

- “AI agents becoming more autonomous”
- “Open-source LLM adoption increasing”

---

## ✅ Personalized Ranking System

Articles are ranked using:

- AI-generated importance score
- historical category preferences

A lightweight personalization layer stores category preferences locally.

---

## ✅ Notion Knowledge Base

Automatically creates:

- article entries
- summaries
- categories
- links
- scores
- weekly insights pages

inside Notion.

---

## ✅ Slack Digest Alerts

Sends a formatted weekly digest notification with:

- top trends
- Notion link
- digest completion confirmation

---

# Workflow Breakdown

---

# 1. Weekly Trigger

## Purpose

Automatically starts the pipeline every week.

## Kestra Component

```yaml
type: io.kestra.plugin.core.trigger.Schedule
```

## Cron

```cron
0 8 * * 0
```

Runs every Sunday at 8 AM.

---

# 2. Fetch News (`fetch_news.py`)

## Purpose

Collects AI/technology articles from RSS feeds.

## Process

- Connects to RSS feeds
- Parses entries
- Extracts:
  - title
  - description
  - link
  - publication date

## Output

```json
fetched_articles.json
```

---

# 3. Deduplication (`deduplicate.py`)

## Purpose

Filters duplicate/similar news stories.

## Logic

Uses:

```python
SequenceMatcher
```

to compare article titles using fuzzy matching.

## Why?

Many tech news outlets repost identical stories.

## Output

```json
unique_articles.json
```

---

# 4. AI Summarization (`summarize.py`)

## Purpose

Transforms raw news into structured intelligence.

## Powered By

- Ollama
- phi3 model

## LLM Tasks

For each article:

- generate summary
- classify category
- assign importance score

## Example Output

```json
{
  "summary": "OpenAI released...",
  "category": "LLMs",
  "importance": 8
}
```

## Defensive Engineering

Handles:

- malformed JSON
- null fields
- model inconsistencies
- timeout fallbacks

## Output

```json
summarized_articles.json
```

---

# 5. Ranking & Personalization (`rank.py`)

## Purpose

Prioritizes the most relevant articles.

## Ranking Formula

```text
Final Score =
AI Importance Score
+
Preference Boost
```

## Personalization

Stores historical category preferences in:

```json
preferences.json
```

Example:

```json
{
  "categories": {
    "LLMs": 5,
    "Agents": 3
  }
}
```

## Output

```json
ranked_articles.json
```

---

# 6. AI Trend Extraction (`insights.py`)

## Purpose

Extracts high-level trends across all articles.

## Input

Combined summaries from ranked articles.

## Example Trends

- AI agents becoming autonomous
- Open-source inference acceleration
- AI infrastructure optimization

## Output

```json
insights.json
```

---

# 7. Notion Upload (`notion_upload.py`)

## Purpose

Stores digest permanently in Notion.

## Database Fields

| Field    | Type   |
| -------- | ------ |
| Title    | Title  |
| Summary  | Text   |
| Link     | URL    |
| Category | Select |
| Score    | Number |

## What Gets Uploaded?

### Articles

- title
- summary
- link
- category
- ranking score

### Weekly Insights

- top 3 trends
- executive summary

## Why Notion?

Acts as:

- searchable knowledge base
- AI research archive
- personal intelligence dashboard

---

# 8. Slack Notification (`slack_notify.py`)

## Purpose

Sends final digest completion notification.

## Includes

- top 3 trends
- Notion link
- digest completion confirmation

## Example Message

```text
🧠 OrchestNews Weekly Digest is Ready!

Top 3 AI Trends:
• Open-source LLM adoption increasing
• AI agents becoming more autonomous
• Inference optimization accelerating

📖 View Full Digest:
https://notion.so/...
```

---

# Why Ollama?

The project intentionally uses local inference instead of cloud APIs.

## Benefits

- Fully free
- Privacy-preserving
- No API costs
- Works offline
- Faster iteration

## Why `phi3` instead of `llama3`?

`phi3` was chosen because:

- lower memory footprint
- faster inference
- more stable for repeated orchestration tasks
- better suited for structured extraction

---

# Error Handling & Reliability

One of the major engineering focuses of the project was defensive orchestration design.

## Problems Handled

- malformed LLM JSON
- null responses
- timeouts
- invalid URLs
- missing article fields
- duplicate content
- Notion schema mismatches

## Reliability Techniques

- `.get()` defensive access
- fallback summaries
- safe type conversion
- bounded prompt sizes
- article limits
- structured logging

---

# Project Learnings

This project demonstrates practical concepts in:

## Workflow Orchestration

Managing dependent multi-step pipelines.

---

## AI Systems Engineering

Working with:

- unreliable LLM outputs
- structured prompting
- fallback handling

---

## Distributed Integrations

Connecting:

- RSS feeds
- local LLMs
- Notion APIs
- Slack APIs

---

## Production Hardening

Handling:

- malformed data
- edge cases
- schema alignment
- operational failures

---

# Future Improvements

## Potential Enhancements

### 🔥 Vector Embeddings

Semantic deduplication using embeddings instead of title similarity.

---

### 🔥 RAG-Based Search

Query historical news archives using semantic retrieval.

---

### 🔥 User Feedback Loop

Allow article rating directly from Slack or Notion.

---

### 🔥 Multi-Agent Pipeline

Separate:

- summarizer agent
- trend analyst agent
- ranking agent

---

### 🔥 Dashboard UI

Build analytics dashboard showing:

- trending categories
- topic evolution
- weekly AI landscape

---

# Why This Project Is Valuable

OrchestNews demonstrates:

- orchestration engineering
- practical AI integration
- local LLM deployment
- automation pipelines
- production debugging
- multi-system architecture

It’s not just a demo project — it mirrors real-world AI workflow systems used in modern engineering organizations.
