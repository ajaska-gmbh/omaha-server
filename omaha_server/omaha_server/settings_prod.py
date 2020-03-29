# coding: utf8

import os

from django.utils import crypto

from furl import furl

from .settings import *
from omaha_server.utils import get_sentry_organization_slug, get_sentry_project_slug

DEBUG = False

ALLOWED_HOSTS = (os.environ.get('HOST_NAME'), '*')
SECRET_KEY = os.environ.get('SECRET_KEY') or crypto.get_random_string(50)

STATICFILES_STORAGE = 'omaha_server.s3utils.StaticS3Storage'
DEFAULT_FILE_STORAGE = 'omaha_server.s3utils.S3Storage'
PUBLIC_READ_FILE_STORAGE = 'omaha_server.s3utils.PublicReadS3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

MEDIA_URL = ''.join([S3_URL, 'media/'])
STATIC_URL = ''.join([S3_URL, 'static/'])

AWS_PRELOAD_METADATA = True
AWS_IS_GZIPPED = True
AWS_DEFAULT_ACL = 'private'


FILEBEAT_HOST = os.environ.get('FILEBEAT_HOST', 'localhost')
FILEBEAT_PORT = os.environ.get('FILEBEAT_PORT', 9021)

CELERYD_HIJACK_ROOT_LOGGER = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'filebeat_format': {
            'format': 'hostname={}|level=%(levelname)s|logger=%(name)s|timestamp=%(asctime)s|module=%(module)s|process=%(process)d|thread=%(thread)d|message=%(message)s'.format(HOST_NAME)
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'celery.beat': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

if FILEBEAT_HOST and FILEBEAT_PORT:
    LOGGING['handlers']['filebeat'] = {
        'level': os.environ.get('FILEBEAT_LOGGING_LEVEL', 'INFO'),
        'class': 'logging.handlers.SysLogHandler',
        'formatter': 'filebeat_format',
        'address': (FILEBEAT_HOST, int(FILEBEAT_PORT))
    }
    LOGGING['root']['handlers'].append('filebeat')
    LOGGING['loggers']['django.request']['handlers'].append('filebeat')

if os.environ.get('CDN_NAME'):
    CDN_NAME = os.environ.get('CDN_NAME')

if CUP_REQUEST_VALIDATION:
    CUP_PEM_KEYS = {
        '1': '/run/secrets/cup_key'
    }
