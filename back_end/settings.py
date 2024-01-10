"""
Django settings for back_end project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import sys
from datetime import timedelta
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

env = environ.Env()
environ.Env.read_env(
    SECRET_KEY=(str, "#l$5e@w!cc9-i1sl$&rf+bjn)1&!&+6&7=inzyav6cwz6)z7c+"),
    DEBUG=(bool, False),
    APPID=(str, ""),
    APP_SECRET=(str, ""),
    DEFAULT_DATABASE=(str, ""),
    REDIS_LOCATION=(str, ""),
    ALIYUN_ENDPOINT=None,
    ALIYUN_INTERNAL_ENDPOINT=None,
    ALIYUN_KEY=None,
    ALIYUN_SECRET=None,
    ALIYUN_BUCKET=None,
    ALIYUN_HOST=None,
    ALIYUN_CDN_STATIC_HOST=None,
    ALIYUN_CDN_MEDIA_HOST=None,
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", bool)

ALLOWED_HOSTS = ["*"]

# Application definition


MY_APPS = [
    "apps.user",
    "apps.draw",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "rest_framework_simplejwt",
    "drf_spectacular",
]

THIRD_PARTY_LOCAL_DEV_APPS = [
    "django_extensions",
    "silk",
]

if DEBUG:
    THIRD_PARTY_APPS += THIRD_PARTY_LOCAL_DEV_APPS

INSTALLED_APPS = (
        [
            "simpleui",
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ]
        + MY_APPS
        + THIRD_PARTY_APPS
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.append('silk.middleware.SilkyMiddleware')

ROOT_URLCONF = "back_end.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "back_end.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {"default": env.db("DEFAULT_DATABASE", "sqlite:///db.sqlite3")}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_LOCATION"),
        "OPTIONS": {
            "db": "1",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "MAX_ENTRIES": 100
        },
        "TIMEOUT": 60,
        "KEY_PREFIX": "AI-APPLET",
        "VERSION": 1.0,
        "KEY_FUNCTION": "utils.utils.make_key",
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"  # 时间设置成中国时间

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DEFAULT_AVATAR = "https://ai-media.xiazq.com/media/avatar.jpg"
AUTH_USER_MODEL = "user.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf.custom_auto_schema.CustomAutoSchema",
    "EXCEPTION_HANDLER": "drf.handler.exception_handler",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "UPLOADED_FILES_USE_URL": False,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "AI-Applet",
    "DESCRIPTION": "ai绘图小程序接口文档",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# 微信小程序
WE_CHAT = {
    "APPID": env("APPID"),  # 小程序ID
    "APP_SECRET": env("APP_SECRET"),  # 小程序SECRET
}

CSRF_TRUSTED_ORIGINS = ["https://ai.xiazq.com"]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
}

# 奖励设置
# 签到奖励
SIGN_IN_REWARD = 1
# 邀请新用户奖励
SHARE_NEW_USER = 1

# stable diffusion 配置
STABLE_DIFFUSION_CONFIG = {
    "sd_model_checkpoint": "LEOSAM HelloWorld 极速版Turbo+LCM_3.0 Turbo+LCM.safetensors [415add75ee]",
    "sd_vae": "Automatic",
    "steps": "8",
    "cfg_scale": "2",
    "seed": "-1",
    "sampler_name": "Euler a",
    "negative_prompt": "",
}

# 阿里云OSS 配置
ALIYUN_OSS_CONFIG = {
    "end_point": env("ALIYUN_ENDPOINT"),
    "end_internal_point": env("ALIYUN_INTERNAL_ENDPOINT"),
    "key": env("ALIYUN_KEY"),
    "secret": env("ALIYUN_SECRET"),
    "bucket": env("ALIYUN_BUCKET"),
    "host": env("ALIYUN_HOST"),
    "cdn_static_host": env("ALIYUN_CDN_STATIC_HOST"),
    "cdn_media_host": env("ALIYUN_CDN_MEDIA_HOST"),
}
ALIYUN_OSS_ENABLE = True
LOCAL_HOST = f"127.0.0.1:{8000 if DEBUG else 9999}"
