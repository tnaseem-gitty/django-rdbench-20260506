DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.gis',
    # 'django.contrib.postgres',
    'django.contrib.admindocs',
    'django.contrib.syndication',
    # 'django.contrib.gis.tests',
    # 'django.contrib.postgres.tests',
    # 'django.contrib.sites.tests',
    # 'django.contrib.flatpages.tests',
    # 'django.contrib.redirects.tests',
    # 'django.contrib.sitemaps.tests',
    # 'django.contrib.humanize.tests',
    'django.contrib.gis.tests',
    # 'django.contrib.postgres.tests',
    'django.contrib.admindocs.tests',
    'django.contrib.syndication.tests',
    'django.contrib.admin.tests',
]

SECRET_KEY = 'fake-key'
