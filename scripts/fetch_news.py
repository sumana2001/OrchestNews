import feedparser
import json

def fetch_rss():
    feeds = [
        "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "https://hnrss.org/frontpage",
        "https://www.technologyreview.com/feed/"
    ]

    articles = []

    for url in feeds:
        parsed = feedparser.parse(url)

        for entry in parsed.entries[:10]:
            articles.append({
                "title": getattr(entry, "title", "No Title"),
                "link": getattr(entry, "link", ""),
                "published": getattr(entry, "published", ""),
                "description": (
                    getattr(entry, "summary", "")
                    or getattr(entry, "description", "")
                )
            })

    print(f"Fetched {len(articles)} articles")

    with open("fetched_articles.json", "w") as f:
        json.dump(articles, f, indent=2)

if __name__ == "__main__":
    fetch_rss()