from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to call backend

@app.route('/format', methods=['POST'])
def format_text():
    data = request.get_json()
    text = data.get('text', '')

    if not text.strip():
        return jsonify({'error': 'Empty input'}), 400

    # Split into sentences and format as bullets
    sentences = [s.strip() for s in text.replace('\n', '.').split('.') if s.strip()]
    return jsonify({'bullets': sentences})

if __name__ == '__main__':
    app.run(debug=True)
