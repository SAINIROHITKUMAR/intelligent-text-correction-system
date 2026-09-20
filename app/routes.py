from flask import Blueprint, jsonify, request
from app.corrector import correct_text

api = Blueprint("api", __name__)

@api.get("/health")
def health():
    return jsonify({"status": "ok", "service": "Intelligent Text Correction System"})

@api.post("/correct")
def correct():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")

    if not isinstance(text, str):
        return jsonify({"error": "text must be a string"}), 400

    if not text.strip():
        return jsonify({"error": "text is required"}), 400

    if len(text) > 5000:
        return jsonify({"error": "text must be 5000 characters or fewer"}), 400

    result = correct_text(text)
    return jsonify(result)
