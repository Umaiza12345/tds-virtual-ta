from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import base64
import pytesseract
from PIL import Image
import io
import google.generativeai as genai
import json

# -----------------------------
# Gemini API Setup
# -----------------------------
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "TDS Virtual TA is running"}

@app.get("/api/")
async def api_info():
    return {
        "message": "Send a POST request to this endpoint with your question and optional image."
    }

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Model
# -----------------------------
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

# -----------------------------
# Search TDS Discussions
# -----------------------------
def find_relevant_posts(question):

    with open("discourse_data.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    matches = []

    question_words = question.lower().split()

    for post in posts:

        score = 0

        content = post["content"].lower()
        title = post["title"].lower()

        for word in question_words:
            if word in content:
                score += 1

            if word in title:
                score += 2

        if score > 0:
            matches.append((score, post))

    matches.sort(reverse=True, key=lambda x: x[0])

    return [post for score, post in matches[:3]]

# -----------------------------
# Main API Endpoint
# -----------------------------
@app.post("/api/")
async def answer_question(data: QuestionRequest):

    extracted_text = ""

    # -------------------------
    # OCR Processing
    # -------------------------
    if data.image:
        try:
            image_data = base64.b64decode(data.image)
            image = Image.open(io.BytesIO(image_data))
            extracted_text = pytesseract.image_to_string(image)

        except Exception as e:
            return {
                "error": f"Image processing failed: {str(e)}"
            }

    # -------------------------
    # Retrieve Relevant Posts
    # -------------------------
    relevant_posts = find_relevant_posts(data.question)

    if relevant_posts:
        context = "\n\n".join(
            [
                f"TITLE: {p['title']}\n"
                f"CONTENT:\n{p['content'][:2000]}"
                for p in relevant_posts
            ]
        )
    else:
        context = "No relevant TDS discussions found."

    # -------------------------
    # Build Prompt
    # -------------------------
    final_prompt = f"""
You are a Teaching Assistant for IIT Madras Tools in Data Science.

Student Question:
{data.question}

Screenshot Text:
{extracted_text}

Relevant TDS Discussions:
{context}

Instructions:
- Use the TDS discussions whenever possible.
- Answer clearly and concisely.
- If the discussion provides the answer, prioritize it.
- If discussions are not sufficient, use your general knowledge.
"""

    try:

        model = genai.GenerativeModel(
            "models/gemini-2.5-flash"
        )

        response = model.generate_content(
            final_prompt
        )

        answer = response.text

        return {
            "answer": answer,
            "links": [
                {
                    "url": p["url"],
                    "text": p["title"]
                }
                for p in relevant_posts
            ]
        }

    except Exception as e:
        return {
            "error": f"Gemini API error: {str(e)}"
        }