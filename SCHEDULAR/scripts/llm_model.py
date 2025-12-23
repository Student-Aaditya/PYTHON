import ollama
import re

# ==================================================
# GLOBAL GREETING HANDLER (USED EVERYWHERE)
# ==================================================
GREETINGS = [
    "hi", "hello", "hey", "namaste",
    "good morning", "good afternoon", "good evening"
]

def is_pure_greeting(text: str) -> bool:
    """
    True only if the message is just a greeting
    (no actual question).
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)

    if text in GREETINGS:
        return True

    # "hi there", "hello bot"
    if len(text.split()) <= 2 and any(text.startswith(g) for g in GREETINGS):
        return True

    return False


def greeting_response(user_text: str) -> str:
    """
    ChatGPT-like greeting response.
    This function is reusable everywhere.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly AI assistant like ChatGPT. "
                "Respond warmly and naturally to greetings. "
                "Keep it short and polite."
            )
        },
        {
            "role": "user",
            "content": user_text
        }
    ]

    response = ollama.chat(
        model="gemma3:1b",
        messages=messages,
        options={
            "temperature": 0.6,
            "num_predict": 30
        }
    )

    return response["message"]["content"].strip()


# ==================================================
# MAIN LLM FUNCTION (USED BY RAG, API, CLI)
# ==================================================
def generate_answer(context: str, question: str) -> str:
    """
    Universal LLM entry point:
    - Handles greetings
    - Enforces RAG context
    - Prevents hallucination
    """

    # 🔥 GREETING SHORT-CIRCUIT (GLOBAL)
    if is_pure_greeting(question):
        return greeting_response(question)

    # ---------------- RAG ANSWER ----------------
    messages = [
        {
            "role": "system",
            "content": (
                "You are a factual college assistant.\n"
                "Answer ONLY using the information in CONTEXT.\n"
                "Do NOT add new facts.\n"
                "If the answer is not present in the context, say:\n"
                "'I don't know based on the available information.'\n"
                "Keep the answer short, clear, and natural."
            )
        },
        {
            "role": "user",
            "content": f"""
CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
        }
    ]

    response = ollama.chat(
        model="gemma3:1b",
        messages=messages,
        options={
            "temperature": 0.2,
            "num_predict": 80
        }
    )

    return response["message"]["content"].strip()
