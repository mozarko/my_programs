# user_auth_jwt_controller.py

from flask import request, jsonify
from domain.jwt_models import JwtRequest, RefreshJwtRequest
from domain.auth_service import AuthService
from domain.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_service = AuthService()


class UserJWTAuthController:

    @staticmethod
    def jwt_register():
        # Реализация регистрации пользователя (например, UserService.register)
        data = request.json
        if not data or "login" not in data or "password" not in data:
            return jsonify({"error": "Invalid request"}), 400
        # Пример: UserService.register возвращает True/False
        success = UserService.register(data["login"], data["password"])
        if not success:
            return jsonify({"error": "User already exists"}), 409
        return jsonify({"message": "User registered"}), 201

    @staticmethod
    def jwt_login():
        data = request.json
        if not data or "login" not in data or "password" not in data:
            return jsonify({"error": "Invalid request"}), 400
        jwt_req = JwtRequest(login=data["login"], password=data["password"])
        jwt_resp = auth_service.login(jwt_req)  # тут генерируется access/refresh token
        if jwt_resp is None:
            return jsonify({"error": "Invalid credentials"}), 401
        return jsonify(jwt_resp.__dict__), 200

    @staticmethod
    def jwt_refresh_access():
        data = request.json
        if not data or "refreshToken" not in data:
            return jsonify({"error": "Invalid request"}), 400
        refresh_req = RefreshJwtRequest(refreshToken=data["refreshToken"])
        jwt_resp = auth_service.refresh_access(refresh_req)
        if jwt_resp is None:
            return jsonify({"error": "Invalid token"}), 401
        return jsonify(jwt_resp.__dict__), 200

    @staticmethod
    def jwt_refresh_refresh():
        data = request.json
        if not data or "refreshToken" not in data:
            return jsonify({"error": "Invalid request"}), 400
        refresh_req = RefreshJwtRequest(refreshToken=data["refreshToken"])
        jwt_resp = auth_service.refresh_refresh(refresh_req)
        if jwt_resp is None:
            return jsonify({"error": "Invalid token"}), 401
        return jsonify(jwt_resp.__dict__), 200

    @staticmethod
    @jwt_required()
    def jwt_user_info():
        user_uuid = get_jwt_identity()
        user = UserService.get_by_uid(user_uuid)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"user_uid": user.uid, "login": user.login})
