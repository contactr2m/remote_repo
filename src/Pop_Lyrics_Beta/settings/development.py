from .base import *             # NOQA
import sys
import logging.config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS'].update({'debug': True})

# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384
if "celery" in sys.argv[0]:
    DEBUG = False

# Django Debug Toolbar
INSTALLED_APPS += (
    'debug_toolbar.apps.DebugToolbarConfig',
    'artist',
    'album',
    'song',
    'videos',
    'news',
    'django.contrib.sites',
    'allauth',
    'allauth_core',
    'bootstrap3',
    'select_multiple_field',

    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',)

# Show emails to console in DEBUG mode
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Show thumbnail generation errors
THUMBNAIL_DEBUG = True

# Log everything to the logs directory at the top
LOGFILE_ROOT = join(dirname(BASE_DIR), 'logs')

# Reset logging
# (see http://www.caktusgroup.com/blog/2015/01/27/Django-Logging-Configuration-logging_config-default-settings-logger/)

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django_log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'project': {
            'handlers': ['proj_log_file'],
            'level': 'DEBUG',
        },
        'werkzeug': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
        },
    }
}

logging.config.dictConfig(LOGGING)

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_AUTO_SIGNUP = False
#   LOGIN_REDIRECT_URL = ''
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_SIGNUP_FORM_CLASS = 'profiles.forms.MyCustomSignupForm'
ACCOUNT_USER_DISPLAY = lambda user: user.get_full_name() or user.email
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

ACCOUNT_FORMS = {
    'login': 'allauth_core.forms.MyLoginForm',
    'signup': 'allauth_core.forms.MySignupForm',
    'add_email': 'allauth_core.forms.MyEmail',
    'change_password': 'allauth_core.forms.MyPasswordChangeForm',
    'reset_password': 'allauth_core.forms.MyPasswordResetForm',
    'set_password': 'allauth_core.forms.MySetPasswordForm',
    'reset_password_from_key': 'allauth_core.forms.MyResetPasswordKeyForm'
}

SOCIALACCOUNT_FORMS = {
    'signup': 'allauth_core.forms.MySocialSignupForm'
}
