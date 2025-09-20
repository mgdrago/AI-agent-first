import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

def tavily_search(query: str, max_results: int = 5) -> List[Dict]:
    """Call Tavily Search API and return simplified list of {title, url}."""
    if DEMO_MODE or not TAVILY_API_KEY:
        return [
            {"title": "AI in Education: 2025 Overview", "url": "https://example.com/ai-edu"},
            {"title": "Mediterranean Diet: Heart Health Meta-Analysis (2024)", "url": "https://example.com/med-diet.pdf"},
            {"title": "UNESCO Report on Digital Learning", "url": "https://example.com/unesco.html"},
        ]
    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "include_answer": False,
                "search_depth": "basic",
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("results", [])[:max_results]:
            results.append({"title": item.get("title") or item.get("url"), "url": item.get("url")})
        return results
    except Exception as e:
        return []
