# Google Gemini LLM API Client with Google Search Grounding

Welcome! This beginner-friendly project demonstrates how to make LLM API calls using Google's `google-genai` SDK with **Google Search Grounding** always enabled.

It formats the LLM's grounded response and web sources into a JSON object that matches the **[Google Custom Search API JSON Response Standard](https://developers.google.com/custom-search/v1/overview)**.

---

## 📚 References & Official Citations

This project is built using official documentation and standards from Google Cloud and Google Developer APIs:

* **Google Cloud Vertex AI & Gemini LLM Documentation**:
  * [Google Cloud Vertex AI Generative AI Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/overview)
  * [Google Search Grounding in Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview)
  * [Google GenAI SDK Python Reference](https://github.com/googleapis/python-genai)
* **Google Custom Search API Reference**:
  * [Google Custom Search JSON API Overview](https://developers.google.com/custom-search/v1/overview)
  * [Google Custom Search API Response Format](https://developers.google.com/custom-search/v1/reference/rest/v1/Search)

---

## 📋 Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Project Structure](#2-project-structure)
3. [Step-by-Step Installation Guide](#3-step-by-step-installation-guide)
4. [How to Get a Gemini API Key](#4-how-to-get-a-gemini-api-key)
5. [Configuration (.env setup)](#5-configuration-env-setup)
6. [Authentication Modes](#6-authentication-modes)
   - [Mode A: Gemini API Key (Recommended for Quick Setup)](#mode-a-gemini-api-key-recommended-for-quick-setup)
   - [Mode B: Google Cloud Vertex AI (Enterprise Setup)](#mode-b-google-cloud-vertex-ai-enterprise-setup)
7. [Running the Python Script](#7-running-the-python-script)
8. [Testing via REST API & cURL](#8-testing-via-rest-api--curl)
9. [Understanding the Response Output](#9-understanding-the-response-output)
10. [Troubleshooting Common Issues](#10-troubleshooting-common-issues)
11. [Citations](#-references--official-citations)

---

## 1. Prerequisites

Before starting, make sure you have:
* **Linux / macOS / Windows Terminal**
* **Python 3.10 or higher** (Check by running `python3 --version`)
* **Google Cloud Project** or a **Gemini API Key** from Google AI Studio

---

## 2. Project Structure

Inside your working directory:

| File / Folder | Purpose |
| :--- | :--- |
| **[.env](file:///usr/local/google/home/elhadik/NIQ_DEMO/.env)** | Configuration file containing API keys, project ID, and model names. Never commit keys to Git! |
| **[requirements.txt](file:///usr/local/google/home/elhadik/NIQ_DEMO/requirements.txt)** | List of Python package dependencies (`google-genai`, `python-dotenv`). |
| **[llm_client.py](file:///usr/local/google/home/elhadik/NIQ_DEMO/llm_client.py)** | Main Python script that queries Gemini LLM and formats the grounded output as Custom Search JSON. |
| **`venv/`** | Virtual environment directory containing isolated Python libraries. |
| **[README.md](file:///usr/local/google/home/elhadik/NIQ_DEMO/README.md)** | This setup guide. |

---

## 3. Step-by-Step Installation Guide

Follow these steps in your terminal:

### Step 1: Open the Project Directory
```bash
cd /usr/local/google/home/elhadik/NIQ_DEMO
```

### Step 2: Create a Virtual Environment
A virtual environment ensures that the packages installed for this project don't conflict with system packages.
```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 4. How to Get a Gemini API Key

If you need a free Gemini API Key, follow these simple steps:

1. **Go to Google AI Studio**: Open your browser and navigate to **[https://aistudio.google.com/](https://aistudio.google.com/)**.
2. **Sign In**: Log in using your Google account.
3. **Navigate to API Keys**: Click on **Get API key** in the left-hand sidebar menu.
4. **Create Key**: Click the **Create API key** button. You can choose to create a key in a new project or select an existing Google Cloud project.
5. **Copy Key**: Copy the generated API key (it will look like `AIzaSy...`).
6. **Save to `.env`**: Paste the key into your `.env` file as shown in the section below.

---

## 5. Configuration (.env setup)

The project reads settings from the `.env` file automatically using `python-dotenv`.

Open [.env](file:///usr/local/google/home/elhadik/NIQ_DEMO/.env) in your editor and configure the fields:

```ini
# --- API Key Mode (Default) ---
GOOGLE_GENAI_USE_VERTEXAI=false
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash

# --- Vertex AI Mode Configuration ---
GOOGLE_CLOUD_PROJECT=shade-sandbox
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_API_USE_CLIENT_CERTIFICATE=false
```

> ⚠️ **Security Tip**: Never share or push `.env` files with secret API keys to public repositories.

---

## 6. Authentication Modes

### Mode A: Gemini API Key (Recommended for Quick Setup)
1. Follow [How to Get a Gemini API Key](#4-how-to-get-a-gemini-api-key) above to get your API key from [Google AI Studio](https://aistudio.google.com/).
2. Set `GOOGLE_GENAI_USE_VERTEXAI=false` in `.env`.
3. Set `GEMINI_API_KEY=AIzaSy...` in `.env`.

### Mode B: Google Cloud Vertex AI (Enterprise Setup)
1. Authenticate with Google Cloud in your terminal:
   ```bash
   gcloud auth application-default login
   ```
2. Set `GOOGLE_GENAI_USE_VERTEXAI=true` in `.env`.
3. Ensure `GOOGLE_CLOUD_PROJECT` matches your active GCP project (e.g., `shade-sandbox`).
4. Read more in the [Google Cloud Vertex AI Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/overview).

---

## 7. Running the Python Script

You can run the script directly with default or custom search prompts.

### Run with Default Prompt:
```bash
./venv/bin/python llm_client.py
```

### Run with a Custom Prompt:
```bash
./venv/bin/python llm_client.py "What are the latest developments in AI technology in 2026?"
```

---

## 8. Testing via REST API & cURL

You can test Google Search Grounding directly using `curl` requests without using Python.

### Option A: Testing via Gemini API Key (Google AI Studio REST API)

Replace `YOUR_GEMINI_API_KEY` with your actual API key:

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key=YOUR_GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "What are the latest developments in generative AI?"
      }]
    }],
    "tools": [{
      "googleSearch": {}
    }]
  }'
```

### Option B: Testing via Google Cloud Vertex AI REST API

If you are using Google Cloud Vertex AI with Application Default Credentials:

```bash
# 1. Get OAuth Access Token
ACCESS_TOKEN=$(gcloud auth application-default print-access-token)
PROJECT_ID="shade-sandbox"
LOCATION="us-central1"
MODEL_ID="gemini-2.5-flash"

# 2. Call Vertex AI Endpoint
curl -X POST "https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/google/models/${MODEL_ID}:generateContent" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "role": "user",
      "parts": [{
        "text": "What are the latest developments in generative AI?"
      }]
    }],
    "tools": [{
      "googleSearch": {}
    }]
  }'
```

---

## 9. Understanding the Response Output

The script outputs a standard JSON object structured after the **[Google Custom Search API Overview](https://developers.google.com/custom-search/v1/overview)**:

```json
{
  "kind": "customsearch#search",
  "url": {
    "type": "application/json",
    "template": "https://www.googleapis.com/customsearch/v1?q={searchTerms}"
  },
  "queries": {
    "request": [
      {
        "title": "Google Custom Search - generative AI trends",
        "totalResults": "5",
        "searchTerms": "generative AI trends",
        "count": 5,
        "startIndex": 1
      }
    ]
  },
  "searchInformation": {
    "searchTime": 3.73,
    "formattedSearchTime": "3.73",
    "totalResults": "5",
    "formattedTotalResults": "5"
  },
  "items": [
    {
      "kind": "customsearch#result",
      "title": "Example Tech News",
      "htmlTitle": "<b>Example Tech News</b>",
      "link": "https://example.com/tech-news",
      "displayLink": "example.com",
      "snippet": "Web source cited for grounding: Example Tech News",
      "htmlSnippet": "Web source cited for grounding: <b>Example Tech News</b>",
      "formattedUrl": "https://example.com/tech-news"
    }
  ],
  "citations": [
    {
      "sourceIndex": 1,
      "title": "Example Tech News",
      "url": "https://example.com/tech-news"
    }
  ],
  "llmResponse": {
    "text": "Generative AI continues to advance rapidly with multi-modal capabilities...",
    "queries": [
      "generative AI trends"
    ]
  }
}
```

---

## 10. Troubleshooting Common Issues

### ❓ Issue 1: `Reauthentication is needed` or `Access Denied`
* **Cause**: Your Google Cloud local credentials expired.
* **Fix**: Run `gcloud auth application-default login` in your terminal, or switch to API Key mode by setting `GOOGLE_GENAI_USE_VERTEXAI=false` and adding `GEMINI_API_KEY` in `.env`.

### ❓ Issue 2: `404 NOT_FOUND. Model not found`
* **Cause**: Model name specified in `.env` is deprecated or unavailable in your region.
* **Fix**: Use supported models in `.env`:
  - `gemini-3.5-flash`
  - `gemini-2.5-flash-lite`

### ❓ Issue 3: `ModuleNotFoundError: No module named 'dotenv'`
* **Cause**: Virtual environment is not activated or dependencies were not installed.
* **Fix**: Run `source venv/bin/activate` and `pip install -r requirements.txt`.

---

Happy coding! 🚀
