import json
import sys
from difflib import SequenceMatcher

def deduplicate_articles():
    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        articles = json.load(f)

    unique_articles = []
    seen_titles = set()

    for article in articles:
        title = article["title"]

        if not any(
            SequenceMatcher(None, title, seen).ratio() > 0.75
            for seen in seen_titles
        ):
            unique_articles.append(article)
            seen_titles.add(title)

    # Keep workflow lightweight
    unique_articles = unique_articles[:6]

    print(f"Unique articles: {len(unique_articles)}")

    with open("unique_articles.json", "w") as f:
        json.dump(unique_articles, f, indent=2)

if __name__ == "__main__":
    deduplicate_articles()