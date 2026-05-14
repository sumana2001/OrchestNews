import json
import os
import sys
import requests

def send_slack_notification():
    insights_file = sys.argv[1]
    notion_status_file = sys.argv[2]

    with open(insights_file, "r") as f:
        insights = json.load(f)

    with open(notion_status_file, "r") as f:
        status = json.load(f)

    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

    notion_url = status.get("url", "Notion link unavailable")

    bullet_trends = "\n".join([
        f"• {trend}" for trend in insights
    ])

    payload = {
        "text": f"""
🧠 OrchestNews Weekly Digest is Ready!

Top 3 AI Trends:
{bullet_trends}

📖 View Full Digest:
{notion_url}
"""
    }

    requests.post(webhook_url, json=payload)

    print("Slack notification sent")

if __name__ == "__main__":
    send_slack_notification()