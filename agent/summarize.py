import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

def summarize_with_llm(query: str, sources: List[Dict], extracted_chunks: List[str]) -> str:
    """Return HTML report string."""
    if DEMO_MODE or (not OPENAI_API_KEY and not GEMINI_API_KEY):
        bullets = "".join([f"<li><strong>Insight {i+1}:</strong> {chunk[:180]}...</li>" for i, chunk in enumerate(extracted_chunks) if chunk][:3])
        links_html = "".join([f"<li><a href='{s['url']}' target='_blank'>{s['title']}</a></li>" for s in sources])
        return f"""
        <h2>Research Brief: {query}</h2>
        <p><em>(Demo mode — replace with real LLM when keys are provided.)</em></p>
        <h3>Key Points</h3>
        <ul>{bullets or '<li>Could not extract content from sources.</li>'}</ul>
        <h3>Sources</h3>
        <ul>{links_html}</ul>
        <p><small>Generated automatically by the AI Research Agent.</small></p>
        """

    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            prompt = f"""
You are a research assistant. Summarize the user's query based on the provided source texts.
Write a concise, structured HTML report with:
- Title
- 4–6 bullet key findings
- A short paragraph of synthesis
- A Sources list with <a> links (use the provided titles/urls)
Query: {query}

Sources Text (truncated):
{ '\n\n---\n\n'.join(t[:2500] for t in extracted_chunks if t) }
            """
            messages = [
                {"role": "system", "content": "You produce clean HTML. No markdown."},
                {"role": "user", "content": prompt},
            ]
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,
            )
            html = completion.choices[0].message.content
            links_html = "".join([f"<li><a href='{s['url']}' target='_blank'>{s['title']}</a></li>" for s in sources])
            return html + f"<h3>Sources</h3><ul>{links_html}</ul>"
        except Exception:
            pass

    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
You are a research assistant. Summarize the user's query based on the provided source texts.
Write a concise, structured HTML report with:
- Title
- 4–6 bullet key findings
- A short paragraph of synthesis
- A Sources list with <a> links (use the provided titles/urls)
Query: {query}

Sources Text (truncated):
{ '\n\n---\n\n'.join(t[:2500] for t in extracted_chunks if t) }
            """
            resp = model.generate_content(prompt)
            html = resp.text
            links_html = "".join([f"<li><a href='{s['url']}' target='_blank'>{s['title']}</a></li>" for s in sources])
            return html + f"<h3>Sources</h3><ul>{links_html}</ul>"
        except Exception:
            pass

    bullets = "".join([f"<li><strong>Insight {i+1}:</strong> {chunk[:180]}...</li>" for i, chunk in enumerate(extracted_chunks) if chunk][:3])
    links_html = "".join([f"<li><a href='{s['url']}' target='_blank'>{s['title']}</a></li>" for s in sources])
    return f"""
    <h2>Research Brief: {query}</h2>
    <p><em>(LLM call failed — showing extracted snippets.)</em></p>
    <h3>Key Points</h3>
    <ul>{bullets or '<li>Could not extract content from sources.</li>'}</ul>
    <h3>Sources</h3>
    <ul>{links_html}</ul>
    """
