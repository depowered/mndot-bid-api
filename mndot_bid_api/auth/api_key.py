"""
Adapted from: https://nilsdebruin.medium.com/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680
"""
import os

from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

from mndot_bid_api import exceptions

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME)


def authorize_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header and api_key_header == API_KEY:
        return api_key_header
    else:
        exceptions.raise_http_403_forbidden()
