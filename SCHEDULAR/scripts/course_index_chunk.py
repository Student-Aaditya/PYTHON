import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = ROOT / "json" / "faq.json"

OUTPUT_PATH = ROOT / "data" / "faq_rag.json"
OUTPUT_PATH.parent.mkdir(exist_ok=True)

INTENT_KEYWORDS = {
    "question":["questions","question","inquiry"],
    "answer":["answer","ask","answers"]
}

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = unescape(text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_course(course: dict):
    result = {
        "question": course.get("question", "").strip()
    }

    for intent in INTENT_KEYWORDS:
        result[intent] = []

    for key, value in course.items():
        if not isinstance(value, str):
            continue

        clean = clean_text(value)
        if len(clean) < 30:
            continue

        key_l = key.lower()
        val_l = clean.lower()

        for intent, keywords in INTENT_KEYWORDS.items():
            if any(k in key_l or k in val_l for k in keywords):
                result[intent].append(clean)

    return {k: v for k, v in result.items() if v}

def build_rag_knowledge():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, dict):
        raw = [raw]

    rag_courses = [extract_course(course) for course in raw]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(rag_courses, f, indent=2, ensure_ascii=False)

    print("✅ RAG knowledge built at:", OUTPUT_PATH)

if __name__ == "__main__":
    build_rag_knowledge()
