import json
import sys

def rank_articles():
    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        articles = json.load(f)

    pref_file = "preferences.json"

    try:
        with open(pref_file, "r") as pf:
            user_prefs = json.load(pf)
    except Exception:
        user_prefs = {
            "categories": {}
        }

    for art in articles:
        category = art.get("category", "AI")

        user_prefs["categories"][category] = (
            user_prefs["categories"].get(category, 0) + 1
        )

        try:
          base_score = int(art.get("importance", 5))
        except Exception:
          base_score = 5

        boost = user_prefs["categories"].get(category, 0)

        art["final_score"] = base_score + (boost * 0.3)

    ranked = sorted(
        articles,
        key=lambda x: x["final_score"],
        reverse=True
    )[:5]

    with open(pref_file, "w") as pf:
        json.dump(user_prefs, pf, indent=2)

    with open("ranked_articles.json", "w") as f:
        json.dump(ranked, f, indent=2)

if __name__ == "__main__":
    rank_articles()