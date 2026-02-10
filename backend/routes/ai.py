import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from backend.ml.predictor import predict_fish
from backend.config import Config


# =========================
# AI BLUEPRINT
# =========================
ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")


# =========================
# PREDICT FISH
# =========================
@ai_bp.route("/predict-fish", methods=["POST"])
@jwt_required()
def predict():

    if "image" not in request.files:
        return jsonify({"message": "No image uploaded"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"message": "Empty filename"}), 400

    filename = secure_filename(image.filename)

    # Ensure upload folder exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    image.save(save_path)

    # 🔮 ML Prediction
    result = predict_fish(save_path)

    return jsonify(result), 200
