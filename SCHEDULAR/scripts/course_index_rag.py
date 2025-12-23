import json
import torch
import faiss
import numpy as np
from pathlib import Path
from transformers import BertTokenizer, BertModel

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "json" / "course.json"
INDEX_DIR = ROOT / "index_store"
INDEX_DIR.mkdir(exist_ok=True)

INDEX_PATH = INDEX_DIR / "faiss_index_course.bin"
META_PATH = INDEX_DIR / "metadata_course.json"

MODEL_NAME = "bert-base-uncased"
MAX_LEN = 256

RELEVANT_KEYS = [
    "course_name",
    "year",
    "semester",
    "about_course",
    "fee_structure",
    "training_workshop",
    "online_admission"
]

# ---------------- LOAD MODEL ----------------
print("🔹 Loading BERT...")
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)
model.eval()

# ---------------- LOAD JSON ----------------
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# ---------------- TEXT + METADATA ----------------
documents = []

for item in data:
    # 🔹 TEXT (this is what BERT embeds)
    text = f"""
    School Name: {item.get('name')}
    Short Name: {item.get('name_short')}
    """

    # 🔹 METADATA (for filtering, source tracking)
    metadata = {k: item.get(k) for k in RELEVANT_KEYS}
    metadata["type"] = "school"
    metadata["source"] = "course.json"

    documents.append({
        "text": text.strip(),
        "metadata": metadata
    })

# ---------------- EMBEDDING FUNCTION ----------------
def embed_text(text: str):
    inputs = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=MAX_LEN,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # CLS token embedding
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

# ---------------- BUILD FAISS INDEX ----------------
print("🔹 Creating embeddings...")
embeddings = []
metadatas = []

for doc in documents:
    emb = embed_text(doc["text"])
    embeddings.append(emb)
    metadatas.append(doc["metadata"])

embeddings = np.array(embeddings).astype("float32")

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# ---------------- SAVE INDEX + METADATA ----------------
faiss.write_index(index, str(INDEX_PATH))

with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(metadatas, f, indent=2, ensure_ascii=False)

print("✅ FAISS index saved:", INDEX_PATH)
print("✅ Metadata saved:", META_PATH)
print(f"📦 Total vectors indexed: {index.ntotal}")
