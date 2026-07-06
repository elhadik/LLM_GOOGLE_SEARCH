import os
import sys
import json
import time
from urllib.parse import urlparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load configuration from .env file
load_dotenv()

def get_client() -> tuple[genai.Client, str]:
    """
    Initializes and returns the Gemini Client and model name based on .env configuration.
    Supports both Google Cloud Vertex AI and Gemini Developer API Key mode.
    """
    use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true").lower() in ("true", "1", "yes")
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    
    if use_vertex:
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        if not project:
            raise ValueError("GOOGLE_CLOUD_PROJECT is required in .env when GOOGLE_GENAI_USE_VERTEXAI=true")
            
        print(f"Initializing Gemini Client via Google Cloud Vertex AI...", file=sys.stderr)
        print(f"  • Project: {project}", file=sys.stderr)
        print(f"  • Location: {location}", file=sys.stderr)
        print(f"  • Model: {model_name}\n", file=sys.stderr)
        
        client = genai.Client(vertexai=True, project=project, location=location)
    else:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required in .env when GOOGLE_GENAI_USE_VERTEXAI=false")
            
        print(f"Initializing Gemini Client via Gemini API Key...", file=sys.stderr)
        print(f"  • Model: {model_name}\n", file=sys.stderr)
        
        client = genai.Client(api_key=api_key)

    return client, model_name

def generate_with_google_search(prompt: str, system_instruction: str = None) -> dict:
    """
    Executes an LLM API call with Google Search tool always enabled.
    Returns a JSON object mimicking Google Custom Search API format (https://developers.google.com/custom-search/v1/overview).
    """
    client, model_name = get_client()
    
    start_time = time.time()
    
    # Always configure Google Search Grounding Tool
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
    if system_instruction:
        config.system_instruction = system_instruction

    print(f"Sending request with Google Search Tool to '{model_name}'...", file=sys.stderr)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config,
    )
    
    elapsed_time = round(time.time() - start_time, 2)

    # Extract grounding metadata
    candidate = response.candidates[0] if response.candidates else None
    grounding_metadata = getattr(candidate, 'grounding_metadata', None) if candidate else None
    
    search_queries = getattr(grounding_metadata, 'web_search_queries', [prompt]) if grounding_metadata else [prompt]
    grounding_chunks = getattr(grounding_metadata, 'grounding_chunks', []) if grounding_metadata else []

    # Map grounding chunks into Google Custom Search Result Items format
    items = []
    citations = []
    
    for idx, chunk in enumerate(grounding_chunks):
        web = getattr(chunk, 'web', None)
        if web:
            url = getattr(web, 'uri', '')
            title = getattr(web, 'title', '')
            parsed_url = urlparse(url)
            display_link = parsed_url.netloc or url
            
            item = {
                "kind": "customsearch#result",
                "title": title,
                "htmlTitle": f"<b>{title}</b>",
                "link": url,
                "displayLink": display_link,
                "snippet": f"Web source cited for grounding: {title}",
                "htmlSnippet": f"Web source cited for grounding: <b>{title}</b>",
                "formattedUrl": url
            }
            items.append(item)
            citations.append({
                "sourceIndex": idx + 1,
                "title": title,
                "url": url
            })

    # Build response formatted to mimic Google Custom Search JSON API
    custom_search_payload = {
        "kind": "customsearch#search",
        "url": {
            "type": "application/json",
            "template": "https://www.googleapis.com/customsearch/v1?q={searchTerms}"
        },
        "queries": {
            "request": [
                {
                    "title": f"Google Custom Search - {q}",
                    "totalResults": str(len(items)),
                    "searchTerms": q,
                    "count": len(items),
                    "startIndex": 1
                } for q in search_queries
            ]
        },
        "searchInformation": {
            "searchTime": elapsed_time,
            "formattedSearchTime": str(elapsed_time),
            "totalResults": str(len(items)),
            "formattedTotalResults": str(len(items))
        },
        "items": items,
        "citations": citations,
        "llmResponse": {
            "text": response.text,
            "queries": search_queries
        }
    }

    return custom_search_payload

if __name__ == "__main__":
    prompt = "What are the latest news and updates about NIQ (NielsenIQ) in 2026?"
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])

    try:
        result_json = generate_with_google_search(prompt)
        print(json.dumps(result_json, indent=2))
    except Exception as e:
        print(f"\n❌ Error during grounded LLM API call: {e}", file=sys.stderr)
        sys.exit(1)
