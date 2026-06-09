import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# SECURITY
# ======================
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
]

# ======================
# APPS
# ======================
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
]

# ======================
# MIDDLEWARE
# ======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================
# CORS
# ======================
CORS_ALLOW_ALL_ORIGINS = True

# ======================
# URLS
# ======================
ROOT_URLCONF = 'voting_project.urls'

# ======================
# TEMPLATES
# ======================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent / 'frontend' / 'public'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ======================
# WSGI
# ======================
WSGI_APPLICATION = 'voting_project.wsgi.application'

# ======================
# DATABASE (POSTGRESQL RENDER)
# ======================
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# ======================
# PASSWORDS
# ======================
AUTH_PASSWORD_VALIDATORS = []

# ======================
# INTERNATIONALIZATION
# ======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================
# STATIC FILES (IMPORTANT FIX)
# ======================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR.parent / 'css',
    BASE_DIR.parent / 'frontend' / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ======================
# MEDIA
# ======================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ======================
# DEFAULT AUTO FIELD
# ======================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================
# CUSTOM
# ======================
ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', 'adminsecret')

# ======================
# DRF
# ======================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    'DEFAULT_PERMISSION_CLASSES': (),
}