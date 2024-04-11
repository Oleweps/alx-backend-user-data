#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash user password"""
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided
    password matches the hashed password.
    """
    return bcrypt.checkpw(str.encode(password), hashed_password)
