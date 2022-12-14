'''
Django settings for djangoapp project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
'''

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import environ
from django.core.management.commands.runserver import Command as runserver

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
runserver.default_port = '8000'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-7=r^71_x5arz64^ni^w-ps_t)q4_99!7^-ynme=pxgkbv-^e$e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = [
    '192.168.146.144',
    '172.18.0.3',
    '172.18.0.4',
    '172.18.0.5',
    'localhost',
    '127.0.0.1',
]
# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'covid_site',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

JAZZMIN_SETTINGS: dict[str, Any] = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    'site_title': 'COVID APP',
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    'site_header': 'COVID APP',
    # CSS classes that are applied to the logo
    'site_logo_classes': None,
    # Welcome text on the login screen
    'welcome_sign': 'Welcome to the COVID APP Admin',
    # Copyright on the footer
    'copyright': 'UAL Ltd',
    # The model admin to search from the search bar, search bar omitted if excluded
    'search_model': 'auth.User',
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    'user_avatar': None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    'topmenu_links': [
        # Url that gets reversed (Permissions can be added)
        {
            'name': 'Home',
            'url': 'admin:index',
            'permissions': ['auth.view_user']
        },
        # model admin to link to (Permissions checked against model)
        {'model': 'auth.User'},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    'usermenu_links': [
        {'model': 'auth.user'},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    'show_sidebar': True,
    # Whether to aut expand the menu
    'navigation_expanded': True,
    # Hide these apps when generating side menu e.g (auth)
    'hide_apps': [],
    # Hide these models when generating side menu (e.g auth.user)
    'hide_models': [],
    # List of apps to base side menu (app or model) ordering off of
    'order_with_respect_to': ['Make Messages', 'auth', ],
    # for the full list of 5.13.0 free icon classes
    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',
        'admin.LogEntry': 'fas fa-file',
    },
    # Icons that are used when one is not manually specified
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    #################
    # Related Modal #
    #################
    # Activate Bootstrap modal
    'related_modal_active': False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    'custom_css': None,
    'custom_js': None,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    'changeform_format': 'horizontal_tabs',
    # override change forms on a per modeladmin basis
    'changeform_format_overrides': {'auth.user': 'collapsible', 'auth.group': 'vertical_tabs'},
}


JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': False,
    'body_small_text': False,
    'brand_small_text': False,
    'brand_colour': False,
    'accent': 'accent-primary',
    'navbar': 'navbar-white navbar-light',
    'no_navbar_border': False,
    'navbar_fixed': False,
    'layout_boxed': False,
    'footer_fixed': False,
    'sidebar_fixed': False,
    'sidebar': 'sidebar-dark-primary',
    'sidebar_nav_small_text': False,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': False,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': False,
    'theme': 'default',
    'button_classes': {
        'primary': 'btn-outline-primary',
        'secondary': 'btn-outline-secondary',
        'info': 'btn-outline-info',
        'warning': 'btn-outline-warning',
        'danger': 'btn-outline-danger',
        'success': 'btn-outline-success',
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'djangoapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'covid_site.views.import_csv',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# reading .env file
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY", default="unsafe-secret-key")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("MYSQL_UALDBUSER_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True
