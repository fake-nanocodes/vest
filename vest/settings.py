"""
Django settings for vest project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import dj_database_url
from pathlib import Path
# import dj_database_url
from pathlib import Path
import os
import environ
env = environ.Env()
# reading .env file
environ.Env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
       'django.contrib.sites',
    'django.contrib.humanize',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'userprofile.apps.UserprofileConfig',
    'deposit.apps.DepositConfig',
    'walletaddress.apps.WalletaddressConfig',
    'withdraw.apps.WithdrawConfig',
    'transfer.apps.TransferConfig',
    'transaction.apps.TransactionConfig',
    'mathfilters',
    'kyc.apps.KycConfig',
    'core.apps.CoreConfig',
    'bonus.apps.BonusConfig',
     'penalty.apps.PenaltyConfig',
     'website.apps.WebsiteConfig',
     'referral.apps.ReferralConfig',
      'contact.apps.ContactConfig',
    'user.apps.UserConfig',
    'investmentplan.apps.InvestmentplanConfig',
    'plan.apps.PlanConfig',
    'faq.apps.FaqConfig',
    'testimony.apps.TestimonyConfig',
    'statistic.apps.StatisticConfig',
    'notification.apps.NotificationConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'vest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.website',
                'website.context_processors.configs',
                'notification.context_processors.notification',
            ],
        },
    },
]

WSGI_APPLICATION = 'vest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASE_URL = env('DATABASE_URL')
DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 2

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = 'optional'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_URL = '/accounts/login'

LOGIN_REDIRECT_URL = '/user/'

#ACCOUNT_SIGNUP_REDIRECT_URL = '/'

CSRF_TRUSTED_ORIGINS = ['https://*.vest-production.up.railway.app']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

#i installed django_smtp_ssl to use 'django_smtp_ssl.SSLEmailBackend'
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# # Custom setting. To email
RECIPIENT_ADDRESS = env('RECIPIENT_ADDRESS')


ACCOUNT_FORMS = {
'signup': 'referral.forms.CustomSignupForm',
}

ACCOUNT_ADAPTER = 'user.adapters.CustomAccountAdapter'


GOOGLE_TRANSLATE_LINK = env('GOOGLE_TRANSLATE_LINK')
CHAT_BOT = env('CHAT_BOT')