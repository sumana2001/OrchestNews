import json
import os
import sys
import requests

NOTION_API_URL = "https://api.notion.com/v1/pages"


def create_notion_page(headers, payload):
    res = requests.post(
        NOTION_API_URL,
        headers=headers,
        json=payload
    )

    print("\n========== NOTION RESPONSE ==========")
    print("STATUS:", res.status_code)
    print(res.text)

    if res.status_code not in (200, 201):
        raise Exception(res.text)

    return res.json()


def upload_to_notion():
    ranked_file = sys.argv[1]
    insights_file = sys.argv[2]

    with open(ranked_file, "r") as f:
        articles = json.load(f)

    with open(insights_file, "r") as f:
        insights = json.load(f)

    token = os.environ.get("NOTION_API_KEY")
    db_id = os.environ.get("NOTION_DATABASE_ID")

    if not token or not db_id:
        raise Exception("Missing Notion credentials")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    print(f"Uploading {len(articles)} articles...")

    # Allowed select options in Notion
    allowed_categories = [
        "LLMs",
        "Agents",
        "Startups",
        "Research",
        "Infra",
        "AI",
        "Summary"
    ]

    for art in articles:
        summary = (
            art.get("summary")
            or art.get("description", "")[:300]
        )

        category = art.get("category") or "AI"

        # Ensure category matches Notion select values
        if category not in allowed_categories:
            category = "AI"

        try:
            score = float(art.get("final_score", 5))
        except Exception:
            score = 5

        link = art.get("link")

        if not link or not str(link).startswith("http"):
            link = None

        payload = {
            "parent": {
                "database_id": db_id
            },
            "properties": {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": f"📰 {art.get('title', 'Untitled Article')}"
                            }
                        }
                    ]
                },
                "Summary": {
                    "rich_text": [
                        {
                            "text": {
                                "content": summary[:2000]
                            }
                        }
                    ]
                },
                "Link": {
                    "url": link
                },
                "Category": {
                    "select": {
                        "name": category
                    }
                },
                "Score": {
                    "number": score
                }
            }
        }

        print("\n========== UPLOADING ARTICLE ==========")
        print(json.dumps(payload, indent=2))

        create_notion_page(headers, payload)

        print(f"Uploaded: {art.get('title', 'Untitled')}")

    # Weekly Insights Summary
    insights_text = "\n".join([
        f"• {trend}" for trend in insights
    ])

    summary_payload = {
        "parent": {
            "database_id": db_id
        },
        "properties": {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": "🏆 Weekly AI Insights"
                        }
                    }
                ]
            },
            "Summary": {
                "rich_text": [
                    {
                        "text": {
                            "content": insights_text[:2000]
                        }
                    }
                ]
            },
            "Category": {
                "select": {
                    "name": "Summary"
                }
            },
            "Score": {
                "number": 10
            }
        }
    }

    res = create_notion_page(headers, summary_payload)

    notion_url = res.get("url", "")

    with open("notion_status.json", "w") as f:
        json.dump({
            "url": notion_url
        }, f)

    print("\nSUCCESS!")
    print("NOTION URL:", notion_url)


if __name__ == "__main__":
    upload_to_notion()