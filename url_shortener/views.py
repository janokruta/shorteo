from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from rest_framework import mixins, viewsets

from url_shortener.models import ShortenedURL
from url_shortener.serializers import ShortenURLSerializer


class ShortenedUrlViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet for handling URL shortening operations.

    Provides endpoints for:
    - Creating new shortened URLs
    - Retrieving original URLs by short code
    """

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenURLSerializer
    lookup_field = "short_code"


class ShortenedUrlRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        shortened_url = get_object_or_404(ShortenedURL, short_code=kwargs["short_code"])
        return shortened_url.original_url
