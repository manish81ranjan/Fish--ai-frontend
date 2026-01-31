import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from ml.predictor import predict_fish
from config import Config

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

@ai_bp.route("/predict-fish", methods=["POST"])
@jwt_required()
def predict():
    if "image" not in request.files:
        return jsonify({"message": "No image uploaded"}), 400

    image = request.files["image"]
    filename = secure_filename(image.filename)

    save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    image.save(save_path)

    result = predict_fish(save_path)

    return jsonify(result), 200
