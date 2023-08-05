import os

from dotenv import find_dotenv, load_dotenv

# take environment variables from .env
load_dotenv(find_dotenv())

# Applications

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "huey.contrib.djhuey",
    "haystack",
    "ordered_model",
    "obapi",
    "obpages",
]

# Secrets
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fake-key")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


# Custom User model
# https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = "obpages.User"


# Debug mode
DEBUG = False

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/


USE_TZ = True

TIME_ZONE = "UTC"

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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

# Haystack settings
# Ignore haystack for now

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.simple_backend.SimpleEngine",
    },
}

# OB Pages

# Results per section for unpaginated lists
OBPAGES_RESULTS_PER_SECTION = 5

# Results per page for paginated lists
OBPAGES_RESULTS_PER_PAGE = 10
