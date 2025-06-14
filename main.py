from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import base64
import pytesseract
from PIL import Image
import io
import openai

# ✅ Set OpenAI Sanand proxy
openai.api_key = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDI5NzhAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.ahEQqUPp0yOwhjVUchlclw2tIkZNyhVmeZ7P3GyhYcQ"
openai.base_url = "https://aiproxy.sanand.workers.dev/v1"

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Allow CORS for Hoppscotch or Promptfoo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define request body schema
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

# ✅ API route
@app.post("/api/")
async def answer_question(data: QuestionRequest):
    extracted_text = ""
    if data.image:
        try:
            image_data = base64.b64decode(data.image)
            image = Image.open(io.BytesIO(image_data))
            extracted_text = pytesseract.image_to_string(image)
        except Exception as e:
            return {"error": f"Image processing failed: {str(e)}"}

    final_prompt = f"""
    Student Question: {data.question}
    Screenshot Text: {extracted_text}

    Based on the TDS course content and Discourse discussions (Jan–Apr 2025), provide a concise answer and include relevant link URLs if known.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": final_prompt}]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        return {"error": f"OpenAI API error: {str(e)}"}

    return {
        "answer": answer,
        "links": [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/sample-post",
                "text": "Related discussion on Discourse"
            }
        ]
    }

# ✅ Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
