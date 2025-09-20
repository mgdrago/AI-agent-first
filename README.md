# AI Research Agent (Flask + SQLite)

A polished, interview-ready implementation of the **AI Agent Intern Take‑Home**:

- **LLM + Exactly 2 tools**: Tavily (Web Search) + Extractor (Trafilatura for HTML, pypdf for PDFs)
- Saves **query + report** in SQLite
- **Attractive web UI** with glassmorphism, gradients, and subtle animations
- **Error handling** with friendly messages
- **History view** and **report view**

> Supports **DEMO_MODE** to run without API keys (handy for an interview demo).

---

## 🧭 Architecture

```
User → Flask (routes)
       ├── agent/search.py      (Tavily web search)
       ├── agent/extract.py     (fetch + Trafilatura/pypdf)
       ├── agent/summarize.py   (LLM: OpenAI or Gemini; DEMO fallback)
       └── agent/db.py          (SQLite: save/list/get reports)
                 ↓
            templates/ (Jinja UI)
```

**Flow**

1. User enters a query on `/`.
2. `tavily_search(query)` finds 2–3 URLs.
3. Each URL → `fetch_and_extract(url)` → clean text (Trafilatura or pypdf).
4. `summarize_with_llm()` generates a **structured HTML report**.
5. The report + links are stored in SQLite (`reports` table).
6. History shows saved queries; click to view a report.

---

## 🛠️ Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with keys; or set DEMO_MODE=true to skip external calls
python app.py
```

Now open http://localhost:5000

---

## 🔑 Environment

```
TAVILY_API_KEY=...

# Choose ONE LLM provider:
OPENAI_API_KEY=...
# OR
GEMINI_API_KEY=...

# Optional:
DEMO_MODE=true   # runs a mock path: fake search results and summary
```

> Interview tip: Set `DEMO_MODE=true` to show the full UX without external dependencies, then disable to show real-time research.

---

## 🧪 Example Queries

- `Latest research on AI in education`
- `Impact of Mediterranean diet on heart health`
- `Does strength training improve sleep quality?`

---

## ❗ Error Handling

- Search fails → flash message: “Search failed or returned no results. Please try again.”
- Extraction fails per-URL → skipped gracefully (still proceeds with others).
- No content extracted → friendly message to try a different query.

---

## 📁 Data Model

`reports (id INTEGER PRIMARY KEY, query TEXT, links TEXT(JSON), report TEXT, created_at TEXT)`

---

## 🎨 UI/UX Notes

- Animated gradient background + subtle grid overlay (content-research theme).
- Glassmorphism cards for transparency, neat contrast on dark theme.
- Clear “30-second guide” on the home page — helps new users.
- Mobile-responsive.

---

## 📹 Demo Recording (≤3 min)

Suggested outline:
1. Enter a query
2. Show results → report generated
3. Click through to report
4. Show history
5. (Optional) Toggle DEMO_MODE off, rerun with real keys

---

## 🤖 Where AI Helped

- Drafted initial system prompts and HTML structure for the summary.
- No AI wrote API keys or secrets.

---

## 📜 License

MIT
