# OrchestNews 🚀

**AI-Powered Weekly Technology Intelligence Pipeline using Kestra + Ollama + Notion + Slack**

---

# Overview

OrchestNews is a fully local, zero-cost workflow orchestration project built using Kestra that automatically generates a weekly AI & technology news digest.

The system fetches trending AI/tech news from RSS feeds, filters duplicate articles, summarizes them using a local LLM running via Ollama, extracts macro-level industry insights, ranks articles using lightweight personalization logic, stores everything in Notion, and finally sends a digest notification through Slack.

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

- Automated weekly AI digest generation.
- Multi-source news aggregation from RSS feeds.
- Duplicate and noise filtering using fuzzy matching.
- Local AI summarization and trend extraction with Ollama.
- Personalized article ranking based on historical preferences.
- Notion integration for storing digests.
- Slack notifications for weekly updates.

---

# Setup and Run Locally

## Prerequisites

1. Install Python 3.9 or higher.
2. Install Kestra locally: [Kestra Installation Guide](https://kestra.io/docs/installation).
3. Install required Python packages:
   ```bash
   pip install feedparser requests
   ```
4. Set up a Notion integration:
   - Create a Notion integration: [Notion Developers](https://developers.notion.com/).
   - Share your database with the integration.
   - Save the API key and database ID.
5. Set up a Slack webhook:
   - Create a Slack app: [Slack Webhooks](https://api.slack.com/messaging/webhooks).
   - Save the webhook URL.

## Configuration

1. Update `notion_upload.py` with your Notion API key and database ID.
2. Update `slack_notify.py` with your Slack webhook URL.

## Running the Workflow

1. Start Kestra:
   ```bash
   kestra server start
   ```
2. Deploy the workflow:
   ```bash
   kestra workflow create workflows/weekly_digest.yaml
   ```
3. Trigger the workflow manually or wait for the scheduled run:
   ```bash
   kestra execution start orchestnews.weekly_digest
   ```

## Running Kestra with Docker Compose

1. Start Kestra using Docker Compose:
   ```bash
   docker-compose up -d
   ```
2. Access the Kestra UI at [http://localhost:8080/ui](http://localhost:8080/ui).
3. Deploy the workflow:
   ```bash
   docker exec -it orchestnews-kestra-1 kestra workflow create /app/storage/workflows/weekly_digest.yaml
   ```
4. Trigger the workflow manually or wait for the scheduled run:
   ```bash
   docker exec -it orchestnews-kestra-1 kestra execution start orchestnews.weekly_digest
   ```

---

# Why This Project Is Valuable

OrchestNews demonstrates:

- Orchestration engineering.
- Practical AI integration.
- Local LLM deployment.
- Automation pipelines.
- Production debugging.
- Multi-system architecture.

It mirrors real-world AI workflow systems used in modern engineering organizations.
