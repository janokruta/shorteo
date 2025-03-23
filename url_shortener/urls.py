from django.urls import include, path
from rest_framework.routers import DefaultRouter

from url_shortener.views import ShortenedUrlRedirectView, ShortenedUrlViewSet

app_name = "url-shortener"

router = DefaultRouter()
router.register(r"urls", ShortenedUrlViewSet, basename="url")

urlpatterns = [
    path("api/", include(router.urls)),
    path("<str:short_code>/", ShortenedUrlRedirectView.as_view(), name="redirect"),
]
