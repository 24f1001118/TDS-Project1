import os
from utils import process_image_text
from dotenv import load_dotenv
load_dotenv()

# Path to all markdown files
COURSE_DIR = "scraped_tds"
DISCOURSE_DIR = "app/data/discourse"

def read_all_markdowns(folder):
    texts = []
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

def get_best_answer(question: str, image_b64: str | None = None) -> str:
    if image_b64:
        image_text = process_image_text(image_b64)
        question += "\n\n" + image_text

    all_course = read_all_markdowns(COURSE_DIR)
    all_forum = read_all_markdowns(DISCOURSE_DIR)
    all_texts = all_course + all_forum

    top_contexts = keyword_search(question, all_texts)

    context = "\n\n---\n\n".join(top_contexts)

    prompt = f"""
You are a helpful AI teaching assistant for the Tools in Data Science course.
Answer the student’s question using only the context below.

CONTEXT:
{context}

QUESTION:
{question}
    """

    # Call OpenAI
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4o-mini"
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()
