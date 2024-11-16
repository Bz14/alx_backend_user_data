#!/usr/bin/env python3
""" Auth module """

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Auth class """
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """ require_auth """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if path[-1] != "/":
            path += "/"
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user """
        return None

    def session_cookie(self, request=None):
        """ Session Cookie """
        if request is None:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'))
