from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status

from url_shortener.models import ShortenedURL
from url_shortener.utils import generate_short_code


class ShortCodeGeneratorTests(TestCase):
    def test_short_code_type(self):
        code = generate_short_code()
        self.assertIsInstance(code, str)

    @parameterized.expand(range(6, 13))
    def test_short_code_valid_length(self, length: int):
        code = generate_short_code(length=length)
        self.assertEqual(len(code), length)

    @parameterized.expand([5, 13])
    def test_short_code_invalid_length(self, length: int):
        with self.assertRaises(ValueError):
            generate_short_code(length=length)


class ShortenedURLViewSetTests(TestCase):
    def test_create_shortened_url_success(self):
        url = reverse("url-shortener:url-list")
        data = {"original_url": "https://example.com/"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        obj = ShortenedURL.objects.get()
        self.assertEqual(len(obj.short_code), 8)
        self.assertEqual(
            response.json().get("short_url"), f"http://testserver/{obj.short_code}"
        )

    def test_create_shortened_url_missing_original_url(self):
        url = reverse("url-shortener:url-list")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json().get("original_url"), ["This field is required."]
        )

    def test_create_shortened_url_invalid_original_url(self):
        url = reverse("url-shortener:url-list")
        data = {"original_url": "invalid-url"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("original_url"), ["Enter a valid URL."])

    @patch("url_shortener.utils._validate_short_code_length")
    def test_create_shortened_url_invalid_code_length(
        self, short_code_validator_mock: Mock
    ):
        short_code_validator_mock.side_effect = ValueError

        url = reverse("url-shortener:url-list")
        data = {"original_url": "https://example.com/"}
        with self.assertRaises(ValueError):
            self.client.post(url, data)

    def test_retrieve_shortened_url_success(self):
        shortened_url_obj = ShortenedURL.objects.create(
            original_url="http://example.com", short_code="testcode"
        )

        url = reverse(
            "url-shortener:url-detail",
            kwargs={"short_code": shortened_url_obj.short_code},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertEqual(
            response_json.get("short_url"),
            f"http://testserver/{shortened_url_obj.short_code}",
        )
        self.assertEqual(
            response_json.get("original_url"), shortened_url_obj.original_url
        )

    def test_retrieve_shortened_url_not_found(self):
        url = reverse("url-shortener:url-detail", kwargs={"short_code": "nonexistent"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_shortened_urls_not_allowed(self):
        url = reverse("url-shortener:url-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_shortened_url_not_allowed(self):
        shortened_url_obj = ShortenedURL.objects.create(
            original_url="http://example.com", short_code="testcode"
        )

        url = reverse(
            "url-shortener:url-detail",
            kwargs={"short_code": shortened_url_obj.short_code},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(
            ShortenedURL.objects.filter(
                short_code=shortened_url_obj.short_code
            ).exists()
        )

    @parameterized.expand(["put", "patch"])
    def test_update_shortened_url_not_allowed(self, method: str):
        shortened_url_obj = ShortenedURL.objects.create(
            original_url="https://example.com", short_code="testcode"
        )

        url = reverse(
            "url-shortener:url-detail",
            kwargs={"short_code": shortened_url_obj.short_code},
        )
        data = {"original_url": "https://updated-example.com"}

        response = getattr(self.client, method)(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        shortened_url_obj.refresh_from_db()
        self.assertEqual(shortened_url_obj.original_url, "https://example.com")


class ShortenedUrlRedirectViewTests(TestCase):
    def test_redirect_to_original_url(self):
        shortened_url_obj = ShortenedURL.objects.create(
            original_url="https://example.com/?qp=val", short_code="testcode"
        )

        url = reverse(
            "url-shortener:redirect",
            kwargs={"short_code": shortened_url_obj.short_code},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, shortened_url_obj.original_url)

    def test_resolve_short_code_not_found(self):
        url = reverse(
            "url-shortener:redirect", kwargs={"short_code": "nonexistent"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
