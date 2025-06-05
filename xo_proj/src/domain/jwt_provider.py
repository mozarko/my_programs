# domain/jwt_provider.py
from flask_jwt_extended import (
    create_access_token, create_refresh_token, decode_token
)
from datetime import timedelta


class JwtProvider:
    @staticmethod
    def generate_access_token(user):
        return create_access_token(
            identity=str(user.uid),
            expires_delta=timedelta(minutes=15)
        )

    @staticmethod
    def generate_refresh_token(user):
        return create_refresh_token(
            identity=str(user.uid),
            expires_delta=timedelta(days=7)
        )

    @staticmethod
    def validate_access_token(token):
        try:
            return decode_token(token)
        except Exception:
            return None

    @staticmethod
    def validate_refresh_token(token):
        try:
            return decode_token(token)
        except Exception:
            return None

    @staticmethod
    def get_uuid_from_token(token):
        try:
            data = decode_token(token)
            return data.get('sub')
        except Exception:
            return None
