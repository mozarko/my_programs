# user_auth_controller.py
from functools import wraps
from flask import request, jsonify, make_response, render_template, session, redirect, url_for
from domain.user_service import UserService
import base64
from tasks import register_user_task  # импорт вверху


class UserAuthController:

    @staticmethod
    def user_register():
        data = request.form
        if not data or 'login' not in data or 'password' not in data:
            return make_response(jsonify({"error": "Invalid request"}), 400)

        # Проверяем успешность регистрации
        # registration_success = UserService().register(data['login'], data['password'])
        result_registartion = register_user_task.delay(data['login'], data['password'])
        registration_success = result_registartion.get(timeout=10)

        print("registr success", registration_success)

        if not registration_success:
            return render_template("user_register.html", registration_error=True)

        return render_template("user_register.html", registration_success=True)

    @staticmethod
    def user_login():
        # Получаем заголовок Authorization
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Basic "):
            # Если заголовка нет или он не начинается с Basic, возвращаем ошибку
            return make_response(jsonify({"error": "Authorization required"}), 401)

        try:
            # Извлекаем строку после "Basic "
            credentials = base64.b64decode(auth_header[6:]).decode("utf-8")
            # Разделяем логин и пароль
            login, password = credentials.split(":", 1)
        except Exception as e:
            return make_response(jsonify({"error": "Invalid authorization header"}), 401)

        # Аутентификация с использованием UserService
        user = UserService().authenticate(login, password)

        if not user:
            # Если пользователь не найден или данные неверны
            return make_response(jsonify({"error": "Invalid credentials"}), 401)

        # Создаем сессию для пользователя
        session['user_uid'] = str(user.uid)
        session['user_login'] = user.login
        session['user_id'] = user.user_id

        # Возвращаем UUID пользователя
        return jsonify({"user_uid": str(user.uid), "login": user.login}), 200

    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_uid' not in session:
                return redirect(url_for('routes.show_login_form'))
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def already_logged_in(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_uid' in session:
                return redirect(url_for('routes.index'))
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def logout():
        session.clear()
        return render_template("index.html")