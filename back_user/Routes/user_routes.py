from flask import Blueprint, request, jsonify
from Services.user_Service import UserService
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from app import db
from dotenv import load_dotenv
import os
import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
import base64
import io
from Services.user_Service import mediapipe_detection
from Services.user_Service import extract_keypoints
from Services.user_Service import model
from Services.user_Service import actions
from Services.user_Service import Image

user_bp = Blueprint("user", __name__)
user_service = UserService()


load_dotenv()

@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data or not data.get("username") or not data.get("email") or not data.get("password"):
            return jsonify({"error": "All fields are required"}), 400

        # Crea un usuario local (no de Google), password obligatorio
        user = User(
            username=data["username"],
            email=data["email"],
            password_hash=data["password"]
        )
        user = user_service.create_user(user, from_google=False)  # ⬅️ Indica que es registro local
        return jsonify({"message": "User created", "user": user.username}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password are required"}), 400

        user = user_service.authenticate_user(data["email"], data["password"])
        if user:
            # Convertimos user.id a string para evitar "Subject must be a string"
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"access_token": access_token}), 200

        return jsonify({"message": "Invalid credentials"}), 401

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/google-login", methods=["POST"])
def google_login():
    try:
        data = request.get_json()
        token = data.get("token")
        if not token:
            return jsonify({"error": "Token is required"}), 400

        # Lee tu Client ID de Google desde variables de entorno
        CLIENT_ID = os.getenv("YOUR_GOOGLE_CLIENT_ID")

        # Verifica el ID token de Google
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            CLIENT_ID,
            clock_skew_in_seconds=10
        )
        email = idinfo.get("email")
        username = idinfo.get("name") or email

        # Busca al usuario por email, si no existe, lo crea sin password local
        user = user_service.get_user_by_email(email)
        if not user:
            user = User(username=username, email=email, password_hash="")
            # Indica que es usuario de Google
            user = user_service.create_user(user, from_google=True)

        # Genera tu token local con Flask-JWT-Extended
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = user_service.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200

@user_bp.route('/api/process_frame', methods=['POST'])
def process_frame():
    # Get the base64 encoded image from the request
    data = request.json
    base64_image = data.get('image', '')
    sequence_data = data.get('sequence', [])
    
    # Decode the base64 image
    img_data = base64.b64decode(base64_image.split(',')[1] if ',' in base64_image else base64_image)
    img = Image.open(io.BytesIO(img_data))
    img_array = np.array(img)
    
    # Process with MediaPipe
    image, results = mediapipe_detection(img_array)
    
    # Extract keypoints
    keypoints = extract_keypoints(results)
    
    # Add to sequence
    sequence = sequence_data.copy()
    sequence.append(keypoints.tolist())
    sequence = sequence[-20:]  # Keep only the last 20 frames
    
    # Make prediction if sequence is complete
    prediction = None
    confidence = 0.0
    
    if len(sequence) == 20:
        # Convert sequence to numpy array and make prediction
        res = model.predict(np.expand_dims(np.array(sequence), axis=0))[0]
        print("Probabilidades:", res)
        print("Argmax:", np.argmax(res))
        print("Max prob:", res[np.argmax(res)])
        prediction = actions[np.argmax(res)]
        confidence = float(res[np.argmax(res)])
    
    # Return the prediction and updated sequence
    return jsonify({
        'prediction': prediction,
        'confidence': confidence,
        'sequence': sequence
    })

# Simple test endpoint
@user_bp.route('/api/test', methods=['GET'])
def test():
    return jsonify({'status': 'API is working'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)