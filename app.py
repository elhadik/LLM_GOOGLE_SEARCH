import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_client import generate_with_google_search

app = Flask(__name__)
CORS(app)

@app.route('/api/search', methods=['GET', 'POST'])
def search_api():
    """
    REST API endpoint that returns Google Search Grounded LLM responses.
    Output is formatted to match the Google Custom Search API JSON response standard.
    """
    prompt = None
    
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        prompt = data.get('prompt') or data.get('q') or data.get('query')
    else:
        prompt = request.args.get('q') or request.args.get('prompt') or request.args.get('query')
        
    if not prompt:
        prompt = "What are the latest developments and trends in AI technology in 2026?"
        
    try:
        response_payload = generate_with_google_search(prompt)
        return jsonify(response_payload), 200
    except Exception as e:
        return jsonify({
            "error": {
                "code": 500,
                "message": str(e),
                "status": "INTERNAL_SERVER_ERROR"
            }
        }), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", "5000"))
    print(f"🚀 Starting LLM Google Search REST API server on http://localhost:{port}/api/search...")
    app.run(host='0.0.0.0', port=port, debug=False)
