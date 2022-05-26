from backend.settings_base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'puppy',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': 'BEI1202jing_'
    }
}
