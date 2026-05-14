import json
import os
import sys
import requests

def extract_insights():
    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        articles = json.load(f)

    combined = "\n".join([
        f"{a.get('title', 'No Title')} - {a.get('summary', '')[:200]}"
        for a in articles
    ])

    prompt = f"""
From the following AI news summaries,
extract the TOP 3 major trends.

{combined}

Return ONLY JSON array.

Example:
[
  "AI agents are becoming more autonomous",
  "Open-source LLM adoption is increasing",
  "Inference optimization is accelerating"
]
"""

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

        output = res.json()["response"]

        print("RAW INSIGHTS:", output)

        start = output.find("[")
        end = output.rfind("]") + 1

        clean = output[start:end]

        trends = json.loads(clean)

    except Exception as e:
        print("Insights generation failed:", e)

        trends = [
            "AI ecosystem continues rapid deployment",
            "Open-source models gaining traction",
            "Inference optimization improving"
        ]

    with open("insights.json", "w") as f:
        json.dump(trends[:3], f, indent=2)

if __name__ == "__main__":
    extract_insights()