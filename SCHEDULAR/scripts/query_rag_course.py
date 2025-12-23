import json
from difflib import SequenceMatcher
from pathlib import Path

from llm_model import generate_answer

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "data" / "course_rag_knowledge.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    COURSES = json.load(f)

import re

SYNONYMS = {
    "fee": ["fees", "cost", "charges", "amount", "price"],
    "career": ["job", "jobs", "scope", "roles", "placement"],
    "training": ["workshop", "workshops", "practical", "hands-on"],
    "eligibility": ["eligible", "criteria", "qualification"],
}

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    for base, words in SYNONYMS.items():
        for w in words:
            text = text.replace(w, base)

    return text

# HELPERS
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_course(question: str):
    q = normalize(question)

    best, score = None, 0.0
    for c in COURSES:
        name = normalize(c.get("course_name", ""))
        s = similarity(q, name)
        if s > score:
            score, best = s, c

    return best if score > 0.4 else None


def detect_intent(question: str):
    q = normalize(question)

    if "fee" in q:
        return "fee"
    if "eligibility" in q:
        return "eligibility"
    if "career" in q:
        return "career"
    if "training" in q:
        return "training"

    return "overview"


# RAG + LLM ANSWER FUNCTION
def answer_question(question: str):
    course = find_course(question)

    if not course:
        return generate_answer("", question)

    intent = detect_intent(question)
    data = course.get(intent)

    if not data:
        return generate_answer("", question)

    context = " ".join(data)
    return generate_answer(context, question)


# TEST
if __name__ == "__main__":
    qs = [
        "hi",
        "how are you",
        "career scope after mtech cse",
        "training workshops in mtech cse",
        "fees for mtech cse",
        "eligibility for mtech computer science",
        "is hostel available?"
    ]

    for q in qs:
        print(f"\nQ: {q}")
        print("A:", answer_question(q))
