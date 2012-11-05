import os
import dj_database_url

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {'default': dj_database_url.config(default='sqlite:////' + os.getcwd() + '/database.db')}

STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

HIGHLIGHTED_COUNTRIES = ['US','HK']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'