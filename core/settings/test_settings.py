from .base import *

# Use an in-memory database for tests (faster than using a real DB)
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',  # Use SQLite in-memory database
}

# Set DEBUG to True to help with debugging tests
DEBUG = True

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
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}

# Use a different email backend for tests (avoid sending real emails)
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Set up the test runner for parallel test execution (optional)
# TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# python manage.py test cart --settings=core.settings.test_settings
# python manage.py makemigrations --settings=core.settings.test_settings