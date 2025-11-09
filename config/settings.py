import os
from pathlib import Path
from urllib.parse import urlparse
from decouple import Config, RepositoryEnv

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# ENVIRONMENT
# ----------------------------
ENV = os.getenv("ENV", "local")

# Determine env file for local development
env_file = BASE_DIR / ".env.local" if ENV == "local" else BASE_DIR / ".env"

# Load environment variables
if env_file.exists():
    config = Config(RepositoryEnv(env_file))
else:
    # Fallback to system environment variables
    config = Config(os.environ)

# ----------------------------
# SECURITY
# ----------------------------
SECRET_KEY = config("SECRET_KEY")
DEBUG = ENV == "local"

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1" if DEBUG else "*"
).split(",")

# ----------------------------
# INSTALLED APPS
# ----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "todo",
    "library",
]

# ----------------------------
# MIDDLEWARE
# ----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ----------------------------
# DATABASE CONFIG
# ----------------------------
DATABASE_URL = config("DATABASE_URL", default=f"sqlite:///{BASE_DIR}/db.sqlite3")

if ENV == "local" or DATABASE_URL.startswith("sqlite"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    parsed = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path[1:],
            "USER": parsed.username,
            "PASSWORD": parsed.password,
            "HOST": parsed.hostname,
            "PORT": parsed.port,
        }
    }

# ----------------------------
# INTERNATIONALIZATION
# ----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------
# STATIC FILES
# ----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
