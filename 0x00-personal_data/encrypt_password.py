#!/usr/bin/env python3
""" Module for storing the hash_password function."""

import bcrypt


def hash_password(password: str) -> bytes:
    """ hashing password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
