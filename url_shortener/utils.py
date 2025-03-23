import random
import string
from typing import cast

from django.conf import settings

from url_shortener.models import ShortenedURL

SHORT_CODE_ALPHABET = string.ascii_letters + string.digits


def generate_short_code(length: int = 8, max_attempts: int = 10) -> str:
    _validate_short_code_length(length)

    attempts = 0
    while attempts < max_attempts:
        attempts += 1

        chars = random.SystemRandom().choices(SHORT_CODE_ALPHABET, k=length)
        short_code = "".join(chars)

        if not ShortenedURL.objects.filter(short_code=short_code).exists():
            return short_code

    return generate_short_code(length=length + 1, max_attempts=max_attempts)


def _validate_short_code_length(length: int) -> None:
    min_length = settings.SHORT_CODE_MIN_LENGTH
    short_code_max_length = cast(int, ShortenedURL.short_code.field.max_length)
    if not min_length <= length <= short_code_max_length:
        raise ValueError(
            f"Length must be between {min_length} and {short_code_max_length}. "
            f"Current length: {length}"
        )
