# 🧠 TDS Virtual TA

This is my submission for the **TDS Virtual TA** project in the IIT Madras Online Degree course **Tools in Data Science (TDS)** (Jan–Apr 2025).

## 🚀 Overview

The **TDS Virtual TA** is an API that helps students by answering questions based on:
- Course materials
- Discourse discussions
- Screenshots (via OCR)

It accepts a text question (and an optional image), extracts any text from the image, and sends a combined prompt to the OpenAI API via **Sanand's AI Proxy**.

## 🛠️ How It Works

- Built using **FastAPI**
- Performs **OCR** using `pytesseract`
- Uses **OpenAI GPT-4o-mini** through Sanand’s Proxy
- Hosted on **Replit**

## 📦 API Endpoint

**POST** `/api/`

### Request Body (JSON):

```json
{
  "question": "What is GA5 bonus criteria?",
  "image": "base64-encoded-image" // optional
}
