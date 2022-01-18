import os

import pytz

UTC = pytz.timezone("UTC")
TIME_ZONE = pytz.timezone("Europe/Moscow")

DEBUG = os.environ.get("DEBUG", None)

SECRET_KEY = "!qfkw7!fpk==%fh3i0jxd51dng^5^(=lcp_vg0=tl#rfv8=rvy"

CELERY_BROKER_URL = "redis://redis:6379/0"

# CORS
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split("|")

# DATABASE
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "db")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE", "postgres")

# TEST_DATABASE
TEST_POSTGRES_HOST = os.environ.get("TEST_POSTGRES_HOST", POSTGRES_HOST)
TEST_POSTGRES_PORT = os.environ.get("TEST_POSTGRES_PORT", POSTGRES_PORT)
TEST_POSTGRES_USER = os.environ.get("TEST_POSTGRES_USER", POSTGRES_USER)
TEST_POSTGRES_PASSWORD = os.environ.get("TEST_POSTGRES_PASSWORD", POSTGRES_PASSWORD)
TEST_POSTGRES_DATABASE = os.environ.get("TEST_POSTGRES_DATABASE", POSTGRES_DATABASE)

MIN_CONNECTIONS_COUNT = os.environ.get("MIN_CONNECTIONS_COUNT", 1)
MAX_CONNECTIONS_COUNT = os.environ.get("MAX_CONNECTIONS_COUNT", 4)

# PATH
API_PREFIX = "/api"

# EMAIL
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")
SERVER_EMAIL = os.getenv("SERVER_EMAIL", "no-reply@mail.idacloud.ru")
DISABLE_EMAIL = os.getenv("DISABLE_EMAIL")

# TELEGRAM
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
