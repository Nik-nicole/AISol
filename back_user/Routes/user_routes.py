from flask import Blueprint, request, jsonify
from Services.user_Service import UserService
from models.user import User
from flask_jwt_extended import create_access_token
from app import db

user_bp = Blueprint("user", __name__)
user_service = UserService()




@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data or not data.get("username") or not data.get("email") or not data.get("password"):
            return jsonify({"error": "All fields are required"}), 400
        user = User(username=data["username"], email=data["email"], password_hash=data["password"])
        user = user_service.create_user(user)
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
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token}), 200
        return jsonify({"message": "Invalid credentials"}), 401
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
