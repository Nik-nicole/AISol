from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from Services.user_Service import UserService

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = UserService.register(data['username'], data['email'], data['password'])
    return jsonify({"message": "Usuario registrado exitosamente", "id": user.id}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token = UserService.login(data['email'], data['password'])
    if token:
        return jsonify({"access_token": token}), 200
    return jsonify({"message": "Credenciales inválidas"}), 401

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = UserService.get_by_id(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 200
