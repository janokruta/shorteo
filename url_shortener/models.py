from django.db import models


class ShortenedURL(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    original_url = models.URLField(max_length=2083)
    short_code = models.CharField(
        max_length=12,
        unique=True,
        db_index=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Shortened URL"
        verbose_name_plural = "Shortened URLs"

    def __str__(self) -> str:
        return f"Shortened URL {self.short_code}"
