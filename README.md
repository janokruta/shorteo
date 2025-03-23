# Shorteo

A URL shortening service built with Django and Django REST Framework.

## Features

- Create shortened URLs through a RESTful API
- Automatic generation of unique short codes
- Redirect to original URLs when accessing a short URL
- Configurable short code length
- Collision handling with increasing code length

## Tech Stack

- Python 3.13
- Django 5.1
- Django REST Framework

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/janokruta/shorteo.git
   cd shorteo
   ```

2. Create and sync environemnt using [uv](https://docs.astral.sh/uv/):
   ```bash
   uv sync
   ```

3. Apply migrations:
   ```bash
   uv run python manage.py migrate
   ```

4. Run the development server:
   ```bash
   uv run python manage.py runserver
   ```

## Usage

### API Endpoints

#### Create a shortened URL

```
POST /api/urls/
```

Request body:
```json
{
  "original_url": "https://example.com/very/long/url/that/needs/shortening"
}
```

Response:
```json
{
  "original_url": "https://example.com/very/long/url/that/needs/shortening",
  "short_url": "http://localhost:8000/abcd1234"
}
```

#### Retrieve original URL info

```
GET /api/urls/{short_code}/
```

Response:
```json
{
  "original_url": "https://example.com/very/long/url/that/needs/shortening",
  "short_url": "http://localhost:8000/abcd1234"
}
```

### Redirect Service

To use a shortened URL, simply access it in a browser or with a request:

```
GET /{short_code}
```

This will redirect to the original URL.

## Project Structure

- `shorteo/` - Main Django project folder
- `url_shortener/` - Django app containing core URL shortening functionality
  - `models.py` - Contains the ShortenedURL model
  - `views.py` - API and redirect views
  - `serializers.py` - REST Framework serializers
  - `utils.py` - Utility functions including short code generation
  - `tests.py` - Comprehensive test suite

## Configuration

You can configure the default short code length in your settings:

```python
# In settings.py
SHORT_CODE_MIN_LENGTH = 6
SHORT_CODE_DEFAULT_LENGTH = 8
```

## Development

### Running Tests

```bash
uv run python manage.py test
```

### Code Style

The project uses Ruff for linting:

```bash
uv run ruff check .
uv run ruff format --check .
```

### Pre-commit

```bash
uv run pre-commit install
```

## Author

Jan Okruta - jan.okruta@gmail.com
