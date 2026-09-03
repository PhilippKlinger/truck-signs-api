"""
Django settings for tsa_app project.
"""

import logging
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

# Configure Django logging
logger = logging.getLogger(__name__)

# Configure logging format
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(funcName)s:%(lineno)d",  # noqa E501
    datefmt="%Y-%m-%d_%H-%M-%S",
)
# path: truck-signs-api/src = root of project tsa_app
BASE_DIR = Path(__file__).resolve().parent.parent
# path: truck-signs-api = root of project truck-signs-api
ROOT_BASE_DIR = BASE_DIR.parent
TEMPLATES_DIR = BASE_DIR / "templates"

# load environment variables from .env file
has_env_vars_configuration = load_dotenv(ROOT_BASE_DIR / ".env")
if not has_env_vars_configuration:
    logger.info("No .env file loaded; using process environment variables.")


def env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean environment variable with strict validation."""
    value = os.getenv(name)
    if value is None:
        return default

    normalized_value = value.strip().lower()
    if normalized_value in {"true", "1", "yes"}:
        return True
    if normalized_value in {"false", "0", "no"}:
        return False
    raise ImproperlyConfigured(f"{name} must be a boolean value.")


def env_list(name: str, default: str = "") -> list[str]:
    """Read a comma-separated environment variable into a clean list."""
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


def required_env(name: str) -> str:
    """Return a required environment value or fail with a clear message."""
    value = os.getenv(name, "").strip()
    if not value:
        raise ImproperlyConfigured(f"Required environment variable {name} is missing.")
    return value


# Read runtime configuration from the environment.
MODE = os.getenv("MODE", "prod").strip().lower()
if MODE not in {"dev", "prod"}:
    raise ImproperlyConfigured("MODE must be either 'dev' or 'prod'.")

DEBUG = env_bool("DEBUG_ENABLED", False)
if MODE == "prod" and DEBUG:
    raise ImproperlyConfigured("DEBUG_ENABLED must be False in production mode.")

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG" if DEBUG else "ERROR").strip().upper()
logger.setLevel(level=LOG_LEVEL)

SECRET_KEY = required_env("SECRET_KEY")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "cloudinary",
    "tsa_products",
    "django.contrib.admin",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tsa_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tsa_app.wsgi.application"

db_engine = "django.db.backends.postgresql" if MODE == "prod" else "django.db.backends.sqlite3"

pg_config = {
    "ENGINE": db_engine,
    "NAME": os.getenv("DB_NAME", "trucksigns_db"),
    "USER": required_env("DB_USER") if MODE == "prod" else os.getenv("DB_USER", ""),
    "PASSWORD": (required_env("DB_PASSWORD") if MODE == "prod" else os.getenv("DB_PASSWORD", "")),
    "HOST": os.getenv("DB_HOST", "db"),
    "PORT": os.getenv("DB_PORT", "5432"),
}

sqlite_config = {
    "ENGINE": db_engine,
    "NAME": BASE_DIR / "db.sqlite3",
}

db_config = sqlite_config if MODE != "prod" else pg_config

DATABASES = {"default": db_config}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles/")

CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS", "http://localhost:3000")

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUD_NAME", ""),
    "API_KEY": os.getenv("CLOUD_API_KEY", ""),
    "API_SECRET": os.getenv("CLOUD_API_SECRET", ""),
}

# Only use Cloudinary in production if configured
if CLOUDINARY_STORAGE["CLOUD_NAME"]:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
