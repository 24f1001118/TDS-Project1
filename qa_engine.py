import os
from utils import process_image_text
from dotenv import load_dotenv
import re
load_dotenv()

# Path to all markdown files
COURSE_DIR = "F:\iitm\python codes\TDS-Project1\scraped_tds"
DISCOURSE_DIR = "F:\iitm\python codes\TDS-Project1\tds_discourse_posts.json"

import re

def extract_links(text: str) -> list[str]:
    return re.findall(r'https?://[^\s"\')>]+', text)

def read_all_markdowns(folder):
    texts = []
    if not os.path.exists(folder):
        print(f"❌ Folder not found: {folder}")
        return []
    for file in os.listdir(folder):
        if file.endswith(".md"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                texts.append(f.read())
    return texts

def keyword_search(question: str, all_texts: list[str], top_k: int = 5):
    scored = []
    for text in all_texts:
        score = sum(1 for word in question.lower().split() if word in text.lower())
        scored.append((score, text))

    # Sort by score descending
    scored.sort(reverse=True, key=lambda x: x[0])
    return [text for score, text in scored[:top_k] if score > 0]

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings

def get_best_answer(question: str, image_b64: str | None = None) -> dict:
    if image_b64:
        image_text = process_image_text(image_b64)
        question += "\n\n" + image_text

    try:
        vectorstore = FAISS.load_local(
            "tds_vector_db",
            SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"),
            allow_dangerous_deserialization=True
        )
        results = vectorstore.similarity_search(question, k=3)
        top_contexts = [doc.page_content for doc in results]

        if not top_contexts:
            return {"answer": "No relevant answer found.", "links": []}

        final_answer = "\n\n---\n\n".join(top_contexts)
        links = extract_links(final_answer)

        return {"answer": final_answer.strip(), "links": links}

    except Exception as e:
        return {"answer": f"Error during search: {str(e)}", "links": []}

