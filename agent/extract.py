import io
from typing import Tuple

import requests
from pypdf import PdfReader
import trafilatura

USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

# Demo fallback snippets keep the UI working when the example.com URLs are used.
DEMO_PAGES = {
    "https://example.com/ai-edu": (
        "Artificial intelligence pilots in classrooms are expanding beyond small trials. "
        "Districts report improvements in formative assessment speed, and teachers note freed "
        "planning time when copilots draft lesson outlines they can refine. Equity concerns persist, "
        "so the leading programs keep a human-in-the-loop for every recommendation and collect "
        "feedback from families."
    ),
    "https://example.com/med-diet.pdf": (
        "A 2024 meta-analysis in cardiology journals reviewed randomized trials of the Mediterranean diet. "
        "Across more than 18,000 participants, adherence to the eating pattern was associated with a 21 percent "
        "reduction in major cardiac events and modest improvements in lipid panels. Researchers highlight the role "
        "of olive oil polyphenols and plant-forward meals in sustaining compliance."
    ),
    "https://example.com/unesco.html": (
        "UNESCO's digital learning brief emphasizes blended models: high-quality content platforms, local facilitation, "
        "and offline synchronisation options for regions with limited bandwidth. Case studies from Kenya and Vietnam show "
        "how microgrants for teacher training helped close the skill gap and lifted course completion rates."
    ),
}


def is_pdf_url(url: str) -> bool:
    return url.lower().endswith(".pdf") or "/pdf" in url.lower()


def fetch_and_extract(url: str) -> Tuple[str, str]:
    """Return (clean_text, error_message). error_message is '' when ok."""
    if url in DEMO_PAGES:
        return DEMO_PAGES[url], ""

    try:
        r = requests.get(url, headers=USER_AGENT, timeout=40, stream=True)
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "").lower()

        if "application/pdf" in content_type or is_pdf_url(url):
            file_bytes = io.BytesIO(r.content)
            reader = PdfReader(file_bytes)
            texts = []
            for page in reader.pages[:10]:
                texts.append(page.extract_text() or "")
            text = "\n".join(texts).strip()
            if not text:
                return "", "PDF text extraction returned empty text."
            return text, ""
        else:
            raw = r.content
            extracted = trafilatura.extract(raw, include_comments=False, include_tables=False)
            if not extracted:
                return "", "Could not extract clean text from HTML."
            return extracted.strip(), ""
    except Exception as e:
        return "", f"Fetch/extract failed: {e}"
