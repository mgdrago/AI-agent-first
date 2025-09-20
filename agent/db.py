import sqlite3
from pathlib import Path
from datetime import datetime
import json

DB_PATH = Path(__file__).resolve().parent.parent / "data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    links TEXT NOT NULL,       -- JSON array of {title, url}
    report TEXT NOT NULL,      -- HTML/Markdown
    created_at TEXT NOT NULL
)""")
    conn.commit()
    conn.close()

def save_report(query: str, links: list, report: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    cur.execute(
        "INSERT INTO reports (query, links, report, created_at) VALUES (?, ?, ?, ?)",
        (query, json.dumps(links, ensure_ascii=False), report, created_at),
    )
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid

def list_reports(limit: int = 50):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, query, created_at FROM reports ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_report(report_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["links"] = json.loads(data["links"])
    return data
