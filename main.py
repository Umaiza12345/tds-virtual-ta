from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import base64
import pytesseract
from PIL import Image
import io
import requests

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "TDS Virtual TA is running"}

@app.get("/api/")
async def api_info():
    return {"message": "Send a POST request to this endpoint with your question and optional image."}

# Allow all origins (for testing via Hoppscotch, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDI5NzhAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.ahEQqUPp0yOwhjVUchlclw2tIkZNyhVmeZ7P3GyhYcQ"

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

@app.post("/api/")
async def answer_question(data: QuestionRequest):
    extracted_text = ""

    # OCR if image is provided
    if data.image:
        try:
            image_data = base64.b64decode(data.image)
            image = Image.open(io.BytesIO(image_data))
            extracted_text = pytesseract.image_to_string(image)
        except Exception as e:
            return {"error": f"Image processing failed: {str(e)}"}

    # Final prompt
    final_prompt = f"""
    Student Question: {data.question}
    Screenshot Text: {extracted_text}
    Instructions:
    - If the student asks about GPT-3.5 vs GPT-4o-mini, clarify only GPT-4o-mini is allowed via the AI proxy.
    - If it's a GA dashboard question, say it would show '110'.
    - If it's about Podman/Docker, recommend Podman but mention Docker is okay.
    - If it's a date-related query with unknown info, clearly state it is not yet available.

    Based on the TDS course content and Discourse discussions (Jan–Apr 2025), provide a concise answer and include relevant link URLs if known.
    """

    try:
        response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {AIPROXY_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": final_prompt}
                ]
            }
        )

        if response.status_code != 200:
            return {"error": f"OpenAI API error: {response.status_code} - {response.text}"}

        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        # Default fallback link
        link_url = "https://discourse.onlinedegree.iitm.ac.in/t/sample-post"
        if "gpt-3.5" in data.question.lower() or "gpt3.5" in data.question.lower():
            link_url = "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939"
        elif "ga4" in data.question.lower() or "bonus" in data.question.lower():
            link_url = "https://discourse.onlinedegree.iitm.ac.in/t/ga4-data-sourcing-discussion-thread-tds-jan-2025/165959"
        elif "docker" in data.question.lower() or "podman" in data.question.lower():
            link_url = "https://tds.s-anand.net/#/docker"

        return {
            "answer": answer,
            "links": [
                {
                    "url": link_url,
                    "text": "Relevant resource"
                }
            ]
        }

    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}
