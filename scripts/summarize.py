import json
import os
import sys
import requests

def ask_ollama(prompt):
    endpoint = os.environ.get(
        "OLLAMA_ENDPOINT",
        "http://host.docker.internal:11434"
    )

    try:
        res = requests.post(
            f"{endpoint}/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        print("STATUS:", res.status_code)

        if res.status_code != 200:
            print("OLLAMA ERROR:", res.text)
            raise Exception(res.text)

        output = res.json()["response"]

        print("RAW OUTPUT:", output[:300])

        return output

    except Exception as e:
        print("OLLAMA FAILED:", str(e))
        raise


def summarize_articles():
    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        articles = json.load(f)

    summarized = []

    for art in articles:
        prompt = f"""
Analyze this AI/tech news article.

TITLE:
{art['title']}

DESCRIPTION:
{art['description'][:500]}

Return ONLY valid JSON.

Example:
{{
  "summary": "Short 2 sentence summary.",
  "category": "LLMs",
  "importance": 8
}}

Rules:
- JSON only
- No markdown
- No explanation
- No extra text
"""

        try:
            response = ask_ollama(prompt)

            start = response.find("{")
            end = response.rfind("}") + 1

            clean_json = response[start:end]

            data = json.loads(clean_json)

        except Exception as e:
            print("JSON parse failed:", e)

            data = {
                "summary": art["description"][:150],
                "category": "AI",
                "importance": 5
            }

        importance = data.get("importance", 5)
        try:
          importance = int(importance)
        except Exception:
          importance = 5
          art.update({
          "summary": data.get("summary",art.get("description", "")[:150]),
          "category": data.get("category", "AI"),
          "importance": importance
          })

        summarized.append(art)

    print(f"Summarized {len(summarized)} articles")

    with open("summarized_articles.json", "w") as f:
        json.dump(summarized, f, indent=2)

if __name__ == "__main__":
    summarize_articles()