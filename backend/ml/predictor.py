import pickle
import json
import os
from PIL import Image
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
INFO_PATH = os.path.join(BASE_DIR, "fish_info.json")

model = None
fish_info = {}

# Load model safely
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    print("⚠️ model.pkl not found — AI will run in demo mode")

# Load fish info safely
if os.path.exists(INFO_PATH):
    with open(INFO_PATH, "r", encoding="utf-8") as f:
        fish_info = json.load(f)


def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB").resize((224, 224))
    img = np.array(img) / 255.0
    return img.reshape(1, 224, 224, 3)


def predict_fish(image_path):
    # Demo fallback if model missing
    if model is None:
        return {
            "fish_name": "Rohu",
            "disease": "Healthy",
            "medicine": "No medicine needed",
            "care": "Keep water clean & oxygenated",
            "confidence": 0.99
        }

    img = preprocess_image(image_path)
    prediction = model.predict(img)
    class_index = int(np.argmax(prediction))

    fish_name = list(fish_info.keys())[class_index]
    info = fish_info.get(fish_name, {})

    return {
        "fish_name": fish_name,
        "disease": info.get("disease", "Healthy"),
        "medicine": info.get("medicine", "No medicine needed"),
        "care": info.get("care", "Maintain good water quality"),
        "confidence": float(np.max(prediction))
    }
