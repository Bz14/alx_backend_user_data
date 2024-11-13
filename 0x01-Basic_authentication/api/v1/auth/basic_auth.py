#!/usr/bin/env python3
"""Basic Auth"""

from .auth import Auth
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base64 authorization header"""

        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        value = authorization_header.split()
        if len(value) != 2:
            return None
        return value[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Decode base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            import base64
            base64_bytes = base64_authorization_header.encode('utf-8')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('utf-8')
            return message
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """ Extract user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        try:
            user_credentials = decoded_base64_authorization_header.split(':')
            return user_credentials[0], user_credentials[1]
        except Exception:
            return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """User object from credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if len(users) <= 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        auth_header = self.authorization_header(request)
        header = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(header)
        email, pwd = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(email, pwd)
        return user
