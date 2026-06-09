# 🧠 TDS Virtual TA

This is my submission for the **TDS Virtual TA** project in the **IIT Madras Online Degree** course **Tools in Data Science (TDS)**.

## 🚀 Overview

The **TDS Virtual TA** is an AI-powered API that helps students by answering questions based on:

- 📚 TDS Discourse discussions
- 🖼️ Screenshots (via OCR)
- 🤖 AI-powered contextual reasoning

The API accepts a text question and an optional image, retrieves the most relevant TDS discussions, extracts text from uploaded images using OCR, and generates a contextual answer using **Google Gemini**.

---

## 🛠️ How It Works

- Built using **FastAPI**
- Performs **OCR** using `pytesseract`
- Retrieves relevant discussions from a scraped TDS Discourse knowledge base
- Uses **Google Gemini** for answer generation
- Returns both an AI-generated answer and relevant discussion links

---

## 🌐 Deployment

**Live API:**

https://tds-virtual-ta-5794.onrender.com

Interactive API Documentation:

https://tds-virtual-ta-5794.onrender.com/docs

---

## 📦 API Endpoint

**POST** `/api/`

### Request Body

```json
{
    "question": "What is GA5 bonus criteria?",
    "image": "base64-encoded-image"
}
```

`image` is optional.

---

## 📤 Example Response

```json
{
    "answer": "The bonus criteria for GA5 are ...",
    "links": [
        {
            "url": "https://discourse.onlinedegree.iitm.ac.in/...",
            "text": "GA5 Discussion Thread"
        }
    ]
}
```

---

## ⚙️ Tech Stack

- Python
- FastAPI
- Google Gemini API
- Pytesseract OCR
- Pillow
- JSON Knowledge Base

---

## 👩‍💻 Author

**Umaiza Fathima**

Built as part of the **Tools in Data Science (TDS)** Virtual TA proj
