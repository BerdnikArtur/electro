from typing import Any

from django.http import HttpRequest

from utils.services.base_service import get_header_and_footer

def register_user_get_context_data(request: HttpRequest, context: dict[str: Any]) -> dict[str: Any]:
    return {**get_header_and_footer(request), **context}

def login_user_get_context_data(request: HttpRequest, context: dict[str: Any]) -> dict[str: Any]:
    return {**get_header_and_footer(request), **context}