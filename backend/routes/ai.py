from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")


# -------------------------------
# HEALTH CHECK
# -------------------------------
@ai_bp.route("/health", methods=["GET"])
def ai_health():
    return jsonify({
        "status": "ok",
        "service": "AI Routes"
    }), 200


# -------------------------------
# AI SUGGESTION ROUTE
# -------------------------------
@ai_bp.route("/suggest", methods=["POST"])
@jwt_required()
def ai_suggest():
    """
    Example input:
    {
        "prompt": "Suggest a luxury watch under 20k"
    }
    """

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or "prompt" not in data:
        return jsonify({
            "error": "Prompt is required"
        }), 400

    prompt = data.get("prompt").strip()

    if not prompt:
        return jsonify({
            "error": "Prompt cannot be empty"
        }), 400

    # -------------------------------
    # MOCK AI LOGIC (Replace later)
    # -------------------------------
    ai_response = generate_mock_ai_response(prompt)

    return jsonify({
        "user_id": user_id,
        "prompt": prompt,
        "response": ai_response
    }), 200


# -------------------------------
# AI CHAT ROUTE
# -------------------------------
@ai_bp.route("/chat", methods=["POST"])
@jwt_required()
def ai_chat():
    """
    Example input:
    {
        "message": "Which watch is best for formal wear?"
    }
    """

    user_id = get_jwt_identity()
    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Message is required"
        }), 400

    reply = generate_mock_ai_response(message)

    return jsonify({
        "user_id": user_id,
        "message": message,
        "reply": reply
    }), 200


# -------------------------------
# MOCK AI FUNCTION
# -------------------------------
def generate_mock_ai_response(text: str) -> str:
    """
    Temporary AI logic.
    Replace this with OpenAI / Gemini / Local LLM later.
    """

    text_lower = text.lower()

    if "watch" in text_lower and "formal" in text_lower:
        return (
            "For formal wear, choose a minimal analog watch with a leather strap "
            "and a slim dial. Black, silver, or brown tones work best."
        )

    if "budget" in text_lower or "under" in text_lower:
        return (
            "You can find great watches under your budget with stainless steel cases, "
            "quartz movement, and sapphire-coated glass."
        )

    if "luxury" in text_lower:
        return (
            "Luxury watches focus on craftsmanship, premium materials, and timeless design. "
            "Automatic movements and sapphire crystal are key features."
        )

    return (
        "I can help you choose watches based on budget, style, occasion, or brand. "
        "Tell me what you're looking for!"
    )
