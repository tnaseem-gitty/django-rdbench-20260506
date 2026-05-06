INSTALLED_APPS = [
    'django.contrib.staticfiles',
]

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

# Use the custom storage class
STATICFILES_STORAGE = 'MyManifestStaticFilesStorage'
