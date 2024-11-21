from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

project_dir = Path(__file__).resolve().parent

def get_log_file_path(app_name, log_filename):
    log_dir = os.path.join(BASE_DIR, app_name, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, log_filename)

def django_logs(log_filename):
    return os.path.join(project_dir,'logs',log_filename)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname} {asctime}] {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # 'django_logs': {
        #     'level': 'ERROR',
        #     'class': 'logging.FileHandler',
        #     'filename': django_logs('django.log'),
        #     'formatter': 'verbose',
        # },
        'file_user_auth': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': get_log_file_path('user_auth', 'user_auth.log'), 
            'formatter': 'verbose',
        },
        'file_user_profiles': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': get_log_file_path('user_profile', 'user_profiles.log'), 
            'formatter': 'verbose',
        },
        'file_order': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': get_log_file_path('order', 'order.log'),
            'formatter': 'verbose',
        },
        'email_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['django_logs'],
        #     'level': 'INFO',
        # },
        'user_auth': {
            'handlers': ['file_user_auth'],
            'level': 'INFO',
            'propagate': False,
        },
        'user_profiles': {
            'handlers': ['file_user_profiles'],
            'level': 'INFO',
            'propagate': False,
        },
        'order': {
            'handlers': ['file_order'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['email_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}