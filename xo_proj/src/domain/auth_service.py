# domain/auth_service.py
from domain.user_service import UserService
from domain.jwt_provider import JwtProvider
from domain.jwt_models import JwtRequest, JwtResponse, RefreshJwtRequest


class AuthService:
    def __init__(self):
        self.user_service = UserService()

    def login(self, jwt_request: JwtRequest) -> JwtResponse | None:
        user = self.user_service.authenticate(jwt_request.login, jwt_request.password)
        if not user:
            return None
        access_token = JwtProvider.generate_access_token(user)
        refresh_token = JwtProvider.generate_refresh_token(user)
        return JwtResponse(type='bearer', accessToken=access_token, refreshToken=refresh_token)

    def refresh_access(self, refresh_jwt_req: RefreshJwtRequest) -> JwtResponse | None:
        data = JwtProvider.validate_refresh_token(refresh_jwt_req.refreshToken)
        if not data:
            return None
        user_uuid = data.get('sub')
        user = self.user_service.get_by_uid(user_uuid)
        access_token = JwtProvider.generate_access_token(user)
        return JwtResponse(type='bearer', accessToken=access_token, refreshToken=refresh_jwt_req.refreshToken)

    def refresh_refresh(self, refresh_jwt_req: RefreshJwtRequest) -> JwtResponse | None:
        data = JwtProvider.validate_refresh_token(refresh_jwt_req.refreshToken)
        if not data:
            return None
        user_uuid = data.get('sub')
        user = self.user_service.get_by_uid(user_uuid)
        access_token = JwtProvider.generate_access_token(user)
        refresh_token = JwtProvider.generate_refresh_token(user)
        return JwtResponse(type='bearer', accessToken=access_token, refreshToken=refresh_token)
