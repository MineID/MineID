import os

from .settings import *

DEBUG = True

# Local database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

try:
    from .local_settings import *
except ImportError:
    pass
