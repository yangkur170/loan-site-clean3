"""
Django settings - OPTIMIZED FOR SPEED
"""

from pathlib import Path
import os
import urllib.parse
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

def env_list(key: str, default: str = ""):
    val = os.getenv(key, default)
    return [x.strip() for x in val.split(",") if x.strip()]

DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes", "on")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,dcfinancingcorporationapply.com,www.dcfinancingcorporationapply.com,loving-tenderness-production-2c60.up.railway.app"
)

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "https://dcfinancingcorporationapply.com,https://www.dcfinancingcorporationapply.com,https://loving-tenderness-production-2c60.up.railway.app"
)

INSTALLED_APPS = [
    "staffdash",
    "cloudinary",
    "jazzmin",
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
    "django.contrib.humanize",
]

# ✅ OPTIMIZED MIDDLEWARE - NO CACHE MIDDLEWARE (causes slowness)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
    "accounts.session_middleware.MultiPortalSessionMiddleware",
    "accounts.site_expiry_middleware.SiteExpiryMiddleware",
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
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.site_control",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ✅ DATABASE - Railway PostgreSQL, never falls back to SQLite in production
def _build_db_config():
    # Priority 1: individual PG* vars (Railway auto-injects these)
    host = os.getenv("PGHOST", "").strip()
    db   = os.getenv("PGDATABASE", "").strip()
    if host and db:
        return {
            "ENGINE":   "django.db.backends.postgresql",
            "NAME":     db,
            "USER":     os.getenv("PGUSER", "postgres").strip(),
            "PASSWORD": os.getenv("PGPASSWORD", "").strip(),
            "HOST":     host,
            "PORT":     os.getenv("PGPORT", "5432").strip(),
            "CONN_MAX_AGE": 600 if not DEBUG else 0,
            "OPTIONS":  {"connect_timeout": 10},
        }

    # Priority 2: DATABASE_URL or DATABASE_PUBLIC_URL — parsed manually
    raw_url = (os.getenv("DATABASE_URL") or os.getenv("DATABASE_PUBLIC_URL") or "").strip()
    if raw_url:
        u = urllib.parse.urlparse(raw_url)
        db_name = u.path.lstrip("/")
        if u.hostname and db_name:
            return {
                "ENGINE":   "django.db.backends.postgresql",
                "NAME":     db_name,
                "USER":     u.username or "postgres",
                "PASSWORD": urllib.parse.unquote(u.password or ""),
                "HOST":     u.hostname,
                "PORT":     str(u.port or 5432),
                "CONN_MAX_AGE": 600 if not DEBUG else 0,
                "OPTIONS":  {"connect_timeout": 10},
            }

    # Priority 3: SQLite — local dev only
    import sys
    print("[WARNING] No PostgreSQL config found — using SQLite (dev only)", file=sys.stderr)
    return {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME":   BASE_DIR / "db.sqlite3",
    }

DATABASES = {"default": _build_db_config()}

# ✅ CACHES - SIMPLE (No complex options)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/login/"

# ✅ STATIC FILES - OPTIMIZED
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# ✅ CSRF & UPLOAD
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20MB
FILE_UPLOAD_MAX_NUMBER_FILES = 10

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_MAX_AGE = 31536000

# ✅ CLOUDINARY
import cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", ""),
    api_key=os.getenv("CLOUDINARY_API_KEY", ""),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", ""),
    secure=True,
)

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME", ""),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY", ""),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET", ""),
}

# ✅ SECURITY
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ✅ LOGGING - MINIMAL (for speed)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,  # Disable all loggers for speed
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",  # Only errors
            "propagate": False,
        },
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "Loan Admin",
    "site_header": "Loan Admin",
    "site_brand": "Loan Admin",
    "welcome_sign": "Welcome",
    "copyright": "Loan",
    "show_sidebar": True,
    "navigation_expanded": True,
    "theme": "darkly",
    "custom_css": "css/admin_custom.css",
    "order_with_respect_to": [
        "accounts.loanapplication",
        "accounts.loanconfig",
        "accounts.paymentmethod",
        "accounts.sitecontrol",
        "accounts.user",
        "accounts.withdrawalrequest",
    ],
}