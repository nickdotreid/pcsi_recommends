import os

DEBUG = False
if 'DEBUG' in os.environ:
	DEBUG = True
	
TEMPLATE_DEBUG = DEBUG

if False not in ( 'STATIC_URL', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_STORAGE_BUCKET_NAME' in os.environ ):
	STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
	STATIC_URL = os.environ['STATIC_URL']
	AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
	AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
	AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

if 'SENDGRID_USERNAME' in os.environ and 'SENDGRID_PASSWORD' in os.environ:
	EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
	EMAIL_HOST= 'smtp.sendgrid.net'
	EMAIL_PORT = 587
	EMAIL_USE_TLS = True
	EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']