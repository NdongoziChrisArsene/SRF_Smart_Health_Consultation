"""
Django settings for smart_health_backend_project (production-ready).
Loads configuration from environment variables (.env recommended).
"""

import os
import logging
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv 
import dj_database_url

# -----------------------
# Load environment variables
# -----------------------
load_dotenv()

# -----------------------
# Paths
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# Logging
# -----------------------
LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR / "logs"))
LOG_DIR.mkdir(exist_ok=True)  # create log dir if missing

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[{asctime}] [{levelname}] {name}: {message}", "style": "{"},
        "simple": {"format": "[{levelname}] {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
        "file": {"class": "logging.FileHandler", "filename": LOG_DIR / "django.log", "formatter": "verbose"},
    },
    "loggers": {
        "notifications": {"handlers": ["console", "file"], "level": LOG_LEVEL, "propagate": False},
        "sms": {"handlers": ["console", "file"], "level": LOG_LEVEL, "propagate": False},
        "email": {"handlers": ["console", "file"], "level": LOG_LEVEL, "propagate": False},
    },
    "root": {"handlers": ["console", "file"], "level": LOG_LEVEL},
}


logger = logging.getLogger(__name__)

# -----------------------
# Environment & secrets
# -----------------------
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()  # development / staging / production

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    if ENVIRONMENT == "production":
        raise RuntimeError("SECRET_KEY must be set in production")
    SECRET_KEY = "dev-fallback-secret-key-change-me"

DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes") and ENVIRONMENT != "production"

# -----------------------
# Installed apps
# -----------------------
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "corsheaders",

    # Project apps
    "users.apps.UsersConfig",
    "patients.apps.PatientsConfig",
    "doctors.apps.DoctorsConfig",
    "appointments.apps.AppointmentsConfig",
    "ai.apps.AiConfig",
    "notifications.apps.NotificationsConfig",
    "reports.apps.ReportsConfig",
]

# -----------------------
# Middleware
# -----------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # must be high in order
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "smart_health_backend_project.urls"

# -----------------------
# Templates
# -----------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "smart_health_backend_project.wsgi.application"

# -----------------------
# Database
# -----------------------
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
    except ImportError as e:
        logger.warning("dj_database_url is not installed. Falling back to env vars: %s", e)
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
                "USER": os.getenv("DATABASE_USER", "postgres"),
                "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
                "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
                "PORT": os.getenv("DATABASE_PORT", "5432"),
            }
        }
    except Exception as e:
        logger.error("Error parsing DATABASE_URL: %s", e)
        raise
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
            "USER": os.getenv("DATABASE_USER", "postgres"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
            "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
            "PORT": os.getenv("DATABASE_PORT", "5432"),
        }
    }

# -----------------------
# Auth
# -----------------------
AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# -----------------------
# REST Framework
# -----------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/min",
        "user": "200/min",
        "ai": os.getenv("AI_THROTTLE_RATE", "10/min"),
    },
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 10)),
}

# -----------------------
# JWT
# -----------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", 60))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("REFRESH_TOKEN_DAYS", 7))),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# -----------------------
# Security
# -----------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = ENVIRONMENT == "production"
CSRF_COOKIE_SECURE = ENVIRONMENT == "production"
SECURE_SSL_REDIRECT = ENVIRONMENT == "production"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", 3600)) if ENVIRONMENT == "production" else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = ENVIRONMENT == "production"
SECURE_HSTS_PRELOAD = ENVIRONMENT == "production"
SECURE_CONTENT_TYPE_NOSNIFF = ENVIRONMENT == "production"

if ENVIRONMENT == "production":
    ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host]
    if not ALLOWED_HOSTS:
        raise RuntimeError("ALLOWED_HOSTS must be set in production")
else:
    ALLOWED_HOSTS = ["*"]

# -----------------------
# CORS
# -----------------------
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if origin]

CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin]

# -----------------------
# Celery (config only)
# -----------------------
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# -----------------------
# Static files
# -----------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static"]

# -----------------------
# Email config (SMTP for Django EmailBackend)
# -----------------------
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() in ("1", "true", "yes")
if EMAIL_PORT == 465:
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")  # SMTP password
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com")

# -----------------------
# SendGrid API key (for sendgrid_service.py)
# -----------------------
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  # separate from SMTP password


# -----------------------
# Misc
# -----------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "smart_health_prod",
        "USER": "prod_user",
        "PASSWORD": "StrongPasswordHere",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

DEBUG = os.environ.get("DEBUG") == "True"
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS", ""
).split(",")

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", ""
).split(",")

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")































# """
# Django settings for smart_health_backend_project (production-ready).
# Loads configuration from environment variables (.env recommended).
# """


# import os
# import logging
# from pathlib import Path
# from datetime import timedelta
# from dotenv import load_dotenv

# # -----------------------
# # Load environment variables
# # -----------------------
# load_dotenv()

# # Setup basic logging 

# BASE_DIR = Path(__file__).resolve().parent.parent

# LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR / "logs"))
# LOG_DIR.mkdir(exist_ok=True)  # create log dir if missing

# LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "[{asctime}] [{levelname}] {name}: {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "[{levelname}] {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "simple",
#         },
#         "file": {
#             "class": "logging.FileHandler",
#             "filename": LOG_DIR / "django.log",
#             "formatter": "verbose",
#         },
#     },
#     "root": {
#         "handlers": ["console", "file"],
#         "level": LOG_LEVEL,
#     },
# }


# # -----------------------
# # Paths
# # -----------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

# # -----------------------
# # Environment & secrets
# # -----------------------
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()  # development / staging / production

# SECRET_KEY = os.getenv("SECRET_KEY")
# if not SECRET_KEY:
#     if ENVIRONMENT == "production":
#         raise RuntimeError("SECRET_KEY must be set in production")
#     SECRET_KEY = "dev-fallback-secret-key-change-me"

# DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes") and ENVIRONMENT != "production"

# # -----------------------
# # Installed apps
# # -----------------------
# INSTALLED_APPS = [
#     # Django apps
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # Third-party
#     "rest_framework",
#     "rest_framework.authtoken",
#     "rest_framework_simplejwt.token_blacklist",
#     "drf_yasg",
#     "corsheaders",

#     # Project apps
#     "users.apps.UsersConfig",
#     "patients.apps.PatientsConfig",
#     "doctors.apps.DoctorsConfig",
#     "appointments",
#     "ai",
#     "notifications",
#     "reports",
# ]

# # -----------------------
# # Middleware
# # -----------------------
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "corsheaders.middleware.CorsMiddleware",  # must be high in order
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "smart_health_backend_project.urls"

# # -----------------------
# # Templates
# # -----------------------
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / "templates"],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = "smart_health_backend_project.wsgi.application"

# # -----------------------
# # Database
# # -----------------------
# DATABASE_URL = os.getenv("DATABASE_URL")
# if DATABASE_URL:
#     try:
#         import dj_database_url
#         DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
#     except ImportError as e:
#         logger.warning("dj_database_url is not installed. Falling back to env vars: %s", e)
#         DATABASES = {
#             "default": {
#                 "ENGINE": "django.db.backends.postgresql",
#                 "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
#                 "USER": os.getenv("DATABASE_USER", "postgres"),
#                 "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
#                 "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
#                 "PORT": os.getenv("DATABASE_PORT", "5432"),
#             }
#         }
#     except Exception as e:
#         logger.error("Error parsing DATABASE_URL: %s", e)
#         raise
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
#             "USER": os.getenv("DATABASE_USER", "postgres"),
#             "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
#             "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
#             "PORT": os.getenv("DATABASE_PORT", "5432"),
#         }
#     }

# # -----------------------
# # Auth
# # -----------------------
# AUTH_USER_MODEL = "users.User"

# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# # -----------------------
# # REST Framework
# # -----------------------
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": (
#         "rest_framework.permissions.IsAuthenticated",
#     ),
#     "DEFAULT_THROTTLE_CLASSES": (
#         "rest_framework.throttling.AnonRateThrottle",
#         "rest_framework.throttling.UserRateThrottle",
#         "rest_framework.throttling.ScopedRateThrottle",
#     ),
#     "DEFAULT_THROTTLE_RATES": {
#         "anon": "20/min",
#         "user": "200/min",
#         "ai": os.getenv("AI_THROTTLE_RATE", "10/min"),
#     },
#     "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 10)),
# }

# # -----------------------
# # JWT
# # -----------------------
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", 60))),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("REFRESH_TOKEN_DAYS", 7))),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
# }

# # -----------------------
# # Security
# # -----------------------
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SESSION_COOKIE_SECURE = ENVIRONMENT == "production"
# CSRF_COOKIE_SECURE = ENVIRONMENT == "production"
# SECURE_SSL_REDIRECT = ENVIRONMENT == "production"
# SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", 3600)) if ENVIRONMENT == "production" else 0
# SECURE_HSTS_INCLUDE_SUBDOMAINS = ENVIRONMENT == "production"
# SECURE_HSTS_PRELOAD = ENVIRONMENT == "production"
# SECURE_CONTENT_TYPE_NOSNIFF = ENVIRONMENT == "production"

# if ENVIRONMENT == "production":
#     ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host]
#     if not ALLOWED_HOSTS:
#         raise RuntimeError("ALLOWED_HOSTS must be set in production")
# else:
#     ALLOWED_HOSTS = ["*"]

# # -----------------------
# # CORS
# # -----------------------
# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True
# else:
#     CORS_ALLOW_ALL_ORIGINS = False
#     CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if origin]

# CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin]

# # -----------------------
# # Celery (config only)
# # -----------------------
# CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"

# # -----------------------
# # Static files
# # -----------------------
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
# if DEBUG:
#     STATICFILES_DIRS = [BASE_DIR / "static"]

# # -----------------------
# # Email config
# # -----------------------
# EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
# EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
# EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() in ("1", "true", "yes")

# # Auto-correct for port 465
# if EMAIL_PORT == 465:
#     EMAIL_USE_TLS = False
#     EMAIL_USE_SSL = True

# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

# # -----------------------
# # Misc
# # -----------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
# USE_I18N = True
# USE_TZ = True
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"












































# """
# Django settings for smart_health_backend_project (production-ready).
# Loads configuration from environment variables (.env recommended).
# """

# from pathlib import Path
# from datetime import timedelta
# import os
# import logging
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv() 

# logger = logging.getLogger(__name__)

# BASE_DIR = Path(__file__).resolve().parent.parent

# # -----------------------
# # Environment & secrets
# # -----------------------
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()  # development / staging / production

# SECRET_KEY = os.getenv("SECRET_KEY")
# if not SECRET_KEY:
#     if ENVIRONMENT == "production":
#         raise RuntimeError("SECRET_KEY must be set in production")
#     # SECRET_KEY = "dev-fallback-secret-key-change-me" 
#     SECRET_KEY ="22n1_(=x7f(75(76d1=&&4+z4is6=rzf73ovcb7tbruh6jpcl!"


# DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes") and ENVIRONMENT != "production"

# # -----------------------
# # Installed apps
# # -----------------------
# INSTALLED_APPS = [
#     # Django apps
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # Third party
#     "rest_framework",
#     "rest_framework.authtoken",
#     "rest_framework_simplejwt.token_blacklist",
#     "drf_yasg",
#     "corsheaders",

#     # Project apps
#     "users.apps.UsersConfig",
#     "patients.apps.PatientsConfig",
#     "doctors.apps.DoctorsConfig",
#     "appointments",
#     "ai",
#     "notifications",
#     "reports",
# ]

# # -----------------------
# # Middleware
# # -----------------------
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "corsheaders.middleware.CorsMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "smart_health_backend_project.urls"

# # -----------------------
# # Templates
# # -----------------------
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / "templates"],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = "smart_health_backend_project.wsgi.application"

# # -----------------------
# # Database
# # -----------------------
# DATABASE_URL = os.getenv("DATABASE_URL")
# if DATABASE_URL:
#     try:
#         import dj_database_url
#         DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
#     except ImportError as e:
#         logger.warning("dj_database_url is not installed. Falling back to env vars. %s", e)
#         DATABASES = {
#             "default": {
#                 "ENGINE": "django.db.backends.postgresql",
#                 "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
#                 "USER": os.getenv("DATABASE_USER", "postgres"),
#                 "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
#                 "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
#                 "PORT": os.getenv("DATABASE_PORT", "5432"),
#             }
#         }
#     except Exception as e:
#         logger.error("Error parsing DATABASE_URL: %s", e)
#         raise
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
#             "USER": os.getenv("DATABASE_USER", "postgres"),
#             "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
#             "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
#             "PORT": os.getenv("DATABASE_PORT", "5432"),
#         }
#     }

# # -----------------------
# # Auth
# # -----------------------
# AUTH_USER_MODEL = "users.User"

# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# # -----------------------
# # REST Framework
# # -----------------------
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": (
#         "rest_framework.permissions.IsAuthenticated",
#     ),
#     "DEFAULT_THROTTLE_CLASSES": (
#         "rest_framework.throttling.AnonRateThrottle",
#         "rest_framework.throttling.UserRateThrottle",
#         "rest_framework.throttling.ScopedRateThrottle",
#     ),
#     "DEFAULT_THROTTLE_RATES": {
#         "anon": "20/min",
#         "user": "200/min",
#         "ai": os.getenv("AI_THROTTLE_RATE", "10/min"),
#     },
#     "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 10)),
# }

# # JWT
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", 60))),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("REFRESH_TOKEN_DAYS", 7))),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
# }

# # -----------------------
# # Security
# # -----------------------
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# if ENVIRONMENT == "production":
#     ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host]
#     if not ALLOWED_HOSTS:
#         raise RuntimeError("ALLOWED_HOSTS must be set in production")
#     print("Production ALLOWED_HOSTS:", ALLOWED_HOSTS)  # temporary debug
# else:
#     ALLOWED_HOSTS = ["*"]

# # -----------------------
# # CORS
# # -----------------------
# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True
# else:
#     CORS_ALLOW_ALL_ORIGINS = False
#     CORS_ALLOWED_ORIGINS = [origin for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if origin]

# CSRF_TRUSTED_ORIGINS = [origin for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin]

# # -----------------------
# # Celery (config only)
# # -----------------------
# CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"

# # -----------------------
# # Static files
# # -----------------------
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
# if DEBUG:
#     STATICFILES_DIRS = [BASE_DIR / "static"]

# # -----------------------
# # Email config
# # -----------------------
# EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
# EMAIL_HOST = os.getenv("EMAIL_HOST", "")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
# EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() in ("1", "true", "yes")

# # Auto-correct for port 465
# if EMAIL_PORT == 465:
#     EMAIL_USE_TLS = False
#     EMAIL_USE_SSL = True


# # -----------------------
# # Misc
# # -----------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
# USE_I18N = True
# USE_TZ = True
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"








































# """
# Django settings for smart_health_backend_project (production-ready).
# Loads configuration from environment variables (.env recommended).
# """

# from pathlib import Path
# from datetime import timedelta
# import os
# from dotenv import load_dotenv 
# from celery import Celery


# # Load .env (if present)
# load_dotenv()

# BASE_DIR = Path(__file__).resolve().parent.parent

# # -----------------------
# # Environment & secrets
# # -----------------------
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()  # development / staging / production

# SECRET_KEY = os.getenv("SECRET_KEY")
# if not SECRET_KEY:
#     if ENVIRONMENT == "production":
#         raise RuntimeError("SECRET_KEY must be set in production")
#     # fallback for local dev only
#     SECRET_KEY = "dev-fallback-secret-key-change-me"

# DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes") and ENVIRONMENT != "production"



# # -----------------------
# # Installed apps
# # -----------------------
# INSTALLED_APPS = [
#     # Django apps
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # Third party
#     "rest_framework",
#     "rest_framework.authtoken",
#     "rest_framework_simplejwt.token_blacklist",
#     "drf_yasg",
#     "corsheaders",            # CORS
#     # Project apps
#     "users.apps.UsersConfig",
#     "patients.apps.PatientsConfig",
#     "doctors.apps.DoctorsConfig",
#     "appointments",
#     "ai",
#     "notifications",
#     "reports",
# ]

# # -----------------------
# # Middleware (note corsheaders early)
# # -----------------------
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "corsheaders.middleware.CorsMiddleware",  # must be high
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "smart_health_backend_project.urls"

# # -----------------------
# # Templates
# # -----------------------
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / "templates"],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = "smart_health_backend_project.wsgi.application"

# # -----------------------
# # Database (production-friendly)
# # -----------------------
# # Use dj-database-url if provided (DATABASE_URL)
# DATABASE_URL = os.getenv("DATABASE_URL")
# if DATABASE_URL:
#     # dj_database_url returns a dict to feed to DATABASES['default']
#     try:
#         import dj_database_url  # pip install dj-database-url
#         DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
#     except Exception:
#         # Fallback: expect manual environment variables below
#         DATABASES = {
#             "default": {
#                 "ENGINE": "django.db.backends.postgresql",
#                 "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
#                 "USER": os.getenv("DATABASE_USER", "postgres"),
#                 "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
#                 "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
#                 "PORT": os.getenv("DATABASE_PORT", "5432"),
#             }
#         }
# else:
#     # Local-style DB settings (safe defaults)
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
#             "USER": os.getenv("DATABASE_USER", "postgres"),
#             "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
#             "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
#             "PORT": os.getenv("DATABASE_PORT", "5432"),
#         }
#     }

# # -----------------------
# # Auth
# # -----------------------
# AUTH_USER_MODEL = "users.User"  

# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]


# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
# ]


# # -----------------------
# # REST Framework (auth, throttling)
# # -----------------------
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": (
#         "rest_framework.permissions.IsAuthenticated",
#     ),
#     "DEFAULT_THROTTLE_CLASSES": (
#         "rest_framework.throttling.AnonRateThrottle",
#         "rest_framework.throttling.UserRateThrottle",
#         "rest_framework.throttling.ScopedRateThrottle",
#     ),
#     "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
#     "DEFAULT_THROTTLE_RATES": {
#         "anon": "20/min",
#         "user": "200/min",
#         "ai": os.getenv("AI_THROTTLE_RATE", "10/min"),
#     },
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 10)),
# }


# # JWT
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("REFRESH_TOKEN_DAYS", "7"))),
# }

# SIMPLE_JWT.update({
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
# })


# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# # -----------------------
# # CORS settings
# # -----------------------
# # Use explicit origins in production; allow-all only when DEBUG True
# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True
# else:
#     CORS_ALLOW_ALL_ORIGINS = False
#     CORS_ALLOWED_ORIGINS = [
#     origin for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if origin
# ]


# CSRF_TRUSTED_ORIGINS = [
#     origin for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin
# ]


# CELERY_BROKER_URL = "redis://localhost:6379/0"
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"



# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_health_backend_project.settings")

# app = Celery("smart_health_backend_project")
# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks()


# # -----------------------
# # Static files
# # -----------------------
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles" 
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
# STATICFILES_DIRS = [BASE_DIR / "static"]


# # -----------------------
# # Email config
# # -----------------------
# EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
# EMAIL_HOST = os.getenv("EMAIL_HOST", "")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

# # -----------------------
# # Gemini / AI key
# # -----------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # -----------------------
# # Security hardening for production
# # -----------------------
# if ENVIRONMENT == "production":
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", 3600))
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
#     SECURE_BROWSER_XSS_FILTER = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
#     ALLOWED_HOSTS = [
#     host for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host
# ]

# else:
#     SECURE_SSL_REDIRECT = False
#     ALLOWED_HOSTS = ["*"]

# # -----------------------
# # Logging (including AI logger)
# # -----------------------
# LOG_DIR = os.getenv("LOG_DIR", BASE_DIR / "logs")
# os.makedirs(LOG_DIR, exist_ok=True)

# LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "standard": {
#             "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "standard",
#         },
#         "file_ai": {
#             "class": "logging.handlers.RotatingFileHandler",
#             "formatter": "standard",
#             "filename": os.path.join(LOG_DIR, "ai.log"),
#             "maxBytes": 10 * 1024 * 1024,  # 10MB
#             "backupCount": 5,
#         },
#         "file_general": {
#             "class": "logging.handlers.RotatingFileHandler",
#             "formatter": "standard",
#             "filename": os.path.join(LOG_DIR, "general.log"),
#             "maxBytes": 10 * 1024 * 1024,
#             "backupCount": 5,
#         },
#     },
#     "loggers": {
#         # AI-specific logger (use in ai views and utils)
#         "ai": {
#             "handlers": ["file_ai", "console"],
#             "level": LOG_LEVEL,
#             "propagate": False,
#         },
#         # General project logger
#         "": {
#             "handlers": ["file_general", "console"],
#             "level": LOG_LEVEL,
#             "propagate": True,
#         },
#     },
# }

# # -----------------------
# # Misc
# # -----------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
# USE_I18N = True
# USE_TZ = True
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"










































