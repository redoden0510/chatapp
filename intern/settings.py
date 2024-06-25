"""
Django settings for intern project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ozyl(r!*=wht$a7^pp+wp=zg5g96yg5wz!7fwe$gq63874z9##'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    
    'django.contrib.sites',    
    'allauth',                 
    'allauth.account',         
    'allauth.socialaccount', 
    
    'debug_toolbar',   
]

# django.contrib.sites用のサイト識別IDを設定
SITE_ID = 1

# 認証バックエンドの設定
AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',   # 一般ユーザー用（メールアドレス認証）
    'django.contrib.auth.backends.ModelBackend',    # 管理サイト用（ユーザー名認証）
)

# 認証方式を「メールアドレス」に設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False    # ユーザー名は使用しない

# サインアップにメールアドレス確認を挟むように設定
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

# LOGIN_REDIRECT_URL = 'index'
# ACCOUNT_LOGOUT_REDIRECT_URL = 'logout'

# 「ログアウト」を一回クリックしただけでログアウトできるように設定
ACCOUNT_LOGOUT_ON_GET = True

# django-allauthが送信するメールの件名に自動付与される接頭辞を空にする設定
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

DEFAULT_FROM_EMAIL = os.environ.get('FROM_EMAIL')

#コンソール上にユーザ登録確認メールを表示。ローカルで確認するため
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    
    'debug_toolbar.middleware.DebugToolbarMiddleware',  
]

ROOT_URLCONF = 'intern.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates', 'allauth')],
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

WSGI_APPLICATION = 'intern.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'mydata',
#         'USER': 'redoden0510',
#         'PASSWORD': 'redoden0510',
#         'HOST': 'database-1.cxagaao49eai.ap-northeast-1.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "vdata", #ご自身が作成したデータベース名
        "USER": "vuser", #ご自身が設定したユーザー名
        "PASSWORD": "redoden0510", #ご自身が設定したパスワード
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "myapp.CustomUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = ''


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = 'friends'
LOGOUT_REDIRECT_URL = "logout"

# デプロイ環境のための設定(追加)
if os.path.isfile('.env'): # .envファイルが存在しない時にもエラーが発生しないようにする
    env = environ.Env(DEBUG=(bool, False),)
    environ.Env.read_env('.env')

    DEBUG = env('DEBUG')
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
    
    
    LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# settings.py
ACCOUNT_FORMS = {
    'login': 'myapp.forms.CustomLoginForm',
    'signup': 'myapp.forms.CustomUserCreationForm',
}

INTERNAL_IPS = [
    '127.0.0.1',
]