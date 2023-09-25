import os
import locale
from pathlib import Path
import environ


from corsheaders.defaults import default_headers

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]
STRIPE_PK = os.environ["stripe_key"]
CHECKOUT_RESPONSE_KEY = os.environ["CHECKOUT_RESPONSE_KEY"]
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ["DEBUG"] == "TRUE")

if DEBUG:
    DEFAULT_DOMAIN = "http://127.0.0.1:8000"
else:
    DEFAULT_DOMAIN = "https://www.leonework.com"

ALLOWED_HOSTS = [
    "51.83.42.186",
    "www.leonework.com",
    "leonework.com",
    "127.0.0.1",
    "186.ip-51-83-42.eu",
]
CSRF_TRUSTED_ORIGINS = ["https://leonework.com", "https://www.leonework.com"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "data_management.apps.DataManagementConfig",
    "welcome_pages.apps.WelcomePagesConfig",
    "students.apps.StudentsConfig",
    "companies.apps.CompaniesConfig",
    "matching.apps.MatchingConfig",
    "home.apps.HomeConfig",
    "payment.apps.PaymentConfig",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap5",
    "django_static_jquery3",
    "debug_toolbar",
    "phonenumber_field",
    "corsheaders",
    "django_static_jquery_ui",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "middleware.JobSelectorMiddleware",
]

ROOT_URLCONF = "_conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "additional_templates/templates")],
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

WSGI_APPLICATION = "_conf.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "leonework",
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ.get("DB_PORT", 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "fr"
try:
    locale.setlocale(locale.LC_TIME, "fr_FR.utf8")
# pylint: disable=bare-except
except:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(Path(__file__).resolve().parent.parent, STATIC_URL)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "welcome_pages.User"
AUTHENTICATION_BACKENDS = ["welcome_pages.backends.EmailBackend"]

INTERNAL_IPS = [
    "127.0.0.1",
]

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "no-reply@leonework.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ["EMAIL_PASSWORD"]

EMAIL_TIMEOUT = 20
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

if os.environ["MAILS"] != "ENABLED":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_URL = "welcome_pages:login"

# paramètres pour utiliser Django-Verify-Email https://pypi.org/project/Django-Verify-Email/
REQUEST_NEW_EMAIL_TEMPLATE = "welcome_pages/email_check/new_email_validation.html"
VERIFICATION_SUCCESS_TEMPLATE = (
    "welcome_pages/email_check/verification_mail_success.html"
)
VERIFICATION_FAILED_TEMPLATE = "welcome_pages/email_check/verification_mail_fail.html"
LINK_EXPIRED_TEMPLATE = "welcome_pages/email_check/link_expired.html"
NEW_EMAIL_SENT_TEMPLATE = "welcome_pages/email_check/new_email_sent.html"
HTML_MESSAGE_TEMPLATE = "mails/email_verification.html"
MAX_RETRIES = 10


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-CSRFTOKEN",
]

STATICFILES_DIRS = [
    BASE_DIR / "additional_static",
]


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

SERVER_EMAIL = EMAIL_HOST_USER
ADMINS = []
EXPIRE_AFTER = "1d"
