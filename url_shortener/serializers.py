from functools import partial
from typing import cast

from django.conf import settings
from rest_framework import serializers
from rest_framework.request import Request

from url_shortener.models import ShortenedURL
from url_shortener.utils import generate_short_code


class ShortenURLSerializer(serializers.ModelSerializer[ShortenedURL]):
    short_code = serializers.HiddenField(
        default=partial(
            generate_short_code,
            length=settings.SHORT_CODE_DEFAULT_LENGTH,
        )
    )
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = ("original_url", "short_code", "short_url")
        read_only_fields = ("short_url",)

    def get_short_url(self, obj: ShortenedURL) -> str:
        request = cast(Request, self.context.get("request"))
        return request.build_absolute_uri(f"/{obj.short_code}")
