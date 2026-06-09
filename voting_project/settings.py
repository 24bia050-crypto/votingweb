import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(**file**).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'change-this-secret-key')

DEBUG = False

ALLOWED_HOSTS = [
'sawaya.pythonanywhere.com',
]

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

MIDDLEWARE = [
'corsheaders.middleware.CorsMiddleware',
'django.middleware.security.SecurityMiddleware',
'whitenoise.middleware.WhiteNoiseMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
"http://localhost:5500",
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'voting_project.urls'

TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [BASE_DIR.parent / 'frontend' / 'public'],
'APP_DIRS': True,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.template.context_processors.static',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
],
},
},
]

WSGI_APPLICATION = 'voting_project.wsgi.application'

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'sawaya$votingdb',
'USER': 'sawaya',
'PASSWORD': 'YOUR_NEW_DATABASE_PASSWORD',
'HOST': 'sawaya.mysql.pythonanywhere-services.com',
'PORT': '3306',
'OPTIONS': {
'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
},
}
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
BASE_DIR.parent / 'css',
BASE_DIR.parent / 'frontend' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', 'adminsecret')

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (),
'DEFAULT_PERMISSION_CLASSES': (),
}
