import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from agent.db import init_db, save_report, list_reports, get_report
from agent.search import tavily_search
from agent.extract import fetch_and_extract
from agent.summarize import summarize_with_llm

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret-change-me")

# Initialize DB
init_db()

@app.get("/")
def index():
    reports = list_reports(limit=100)
    return render_template("index.html", reports=reports)

@app.post("/search")
def do_search():
    query = request.form.get("query", "").strip()
    if not query:
        flash("Please enter a query.", "error")
        return redirect(url_for("index"))

    # 1) Search
    sources = tavily_search(query, max_results=3)
    if not sources:
        flash("Search failed or returned no results. Please try again.", "error")
        return redirect(url_for("index"))

    # 2) Extract
    extracted = []
    kept_sources = []
    for s in sources:
        text, err = fetch_and_extract(s["url"])
        if text:
            extracted.append(text)
            kept_sources.append(s)
        else:
            print(f"[WARN] Skipping source due to extraction error: {s['url']} -> {err}")

    if not extracted:
        flash("Could not extract content from the found pages. Try a different query.", "error")
        return redirect(url_for("index"))

    # 3) Summarize
    html_report = summarize_with_llm(query, kept_sources, extracted)

    # 4) Save
    rid = save_report(query=query, links=kept_sources, report=html_report)
    flash("Report generated and saved!", "success")
    return redirect(url_for("view_report", report_id=rid))

@app.get("/report/<int:report_id>")
def view_report(report_id: int):
    data = get_report(report_id)
    if not data:
        flash("Report not found.", "error")
        return redirect(url_for("index"))
    return render_template("report.html", report=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
