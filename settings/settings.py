# Django settings for Anou project.
import dj_database_url, os, socket
from memcacheify import memcacheify
from people import *

LOCAL_MACHINES = ['TOMCOUNSELL']

PRODUCTION = STAGE = DEMO = False

if 'NAME' in os.environ and os.environ['NAME'] == 'anou-cobra':
  PRODUCTION = True
elif 'NAME' in os.environ and os.environ['NAME'] == 'anou-cobra-stage':
  STAGE = True
elif 'NAME' in os.environ and os.environ['NAME'] == 'anou-cobra-demo':
  DEMO = True
else: #probably on LOCAL_MACHINES
  pass

PAYMENTS_PRODUCTION = PRODUCTION
DEBUG = not (PRODUCTION or DEMO)
TEMPLATE_DEBUG = not (STAGE or PRODUCTION or DEMO)

ANOU_FEE_RATE = 0.10
DAYS_UNTIL_PRODUCT_EXPIRES = 120

UNDER_CONSTRUCTION = False
INTERNAL_IPS = ('127.0.0.1',)
SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

ADMINS = (('Developer', 'dev@theanou.com'),)
MANAGERS = ADMINS

if PRODUCTION or STAGE or DEMO:
  DATABASES = {'default': dj_database_url.config()}
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
  DATABASES = {
    'default': {
      'ENGINE':   'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
      'NAME':     'cobra',                      # Or path to database file if using sqlite3.
      'USER':     'Cobra',                      # Not used with sqlite3.
      'PASSWORD': '4WuPb3eMDyfByVBs',           # Not used with sqlite3.
      'HOST':     '',                           # Set to empty string for localhost. Not used with sqlite3.
      'PORT':     '',                           # Set to empty string for default. Not used with sqlite3.
    }
  }

################## 3RD PARTY SERVICES ##################

#these should all be environment variables, ideally

#AMAZON WEB STORAGE S3, STATIC FILE HOSTING
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAISBCAIGR4FHXJKBQ'
AWS_SECRET_ACCESS_KEY = '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'
if PRODUCTION:
  AWS_STORAGE_BUCKET_NAME = 'anou'
elif DEMO:
  AWS_STORAGE_BUCKET_NAME = 'anou-demo'
else:
  AWS_STORAGE_BUCKET_NAME = 'anou-stage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

#CLOUDINARY IMAGE AND PHOTO HOSTING
if PRODUCTION or STAGE or DEMO:
  CLOUDINARY = {
    'cloud_name':     'hork5h8x1',
    'api_key':        '697913462329845',
    'api_secret':     '-dc1wU2_xyJmYaeJP1Yimn2-cuA',
    'format':         'jpg',
    'transformation': 't_original',
    'upload_url':     'http://api.cloudinary.com/v1_1/hork5h8x1/image/upload/',
    'download_url':   'http://res.cloudinary.com/hork5h8x1/image/upload/'
  }
else:
  CLOUDINARY = {
    'cloud_name':     'anou',
    'api_key':        '155257496663982',
    'api_secret':     'z78hCbzKQ26-6UQoE0FvmguCP9A',
    'format':         'jpg',
    'transformation': 't_original',
    'upload_url':     'http://api.cloudinary.com/v1_1/anou/image/upload/',
    'download_url':   'http://res.cloudinary.com/anou/image/upload/'
  }

#SENDGRID EMAIL BACKEND
EMAIL_HOST          = 'smtp.sendgrid.net'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True

if PRODUCTION:
  EMAIL_HOST_USER     = 'app15107937@heroku.com'
  EMAIL_HOST_PASSWORD = 'tmuipovc'
else:
  EMAIL_HOST_USER     = 'limetree'
  EMAIL_HOST_PASSWORD = 'H0hner765@'

#TELERIVET SMS GATEWAY
if PRODUCTION:
  TELERIVET = {
    'api_key':          'DF6UFT49DW643UQWDC436PC2K6LKWEDC',
    'project_id':       'PJb41b4e785d567945065e25271c8bd1dd',
    'phone_id':         'PNe5ceaab258b60afe79687a5620c5c265',
    'phone_number':     '212637637566',#2120623809088
    'status_url':       'http://www.theanou.com/communication/sms/status_confirmation',
    'status_secret':    'JuiceIsWorthTheSqueeze',
    'webhook_url':      'http://www.theanou.com/communication/sms/incoming',
    'webhook_secret':   'NT9NAEQUAGWWGG4WQ7GQHP7WHXPNZR3P'
  }
elif DEMO:
  TELERIVET = {
    'api_key':          'H3P3UPFQ2CKMXLDLFX446FCPXMDK42CL',
    'project_id':       'PJ6ff0b172f5c2b56a',
    'phone_id':         'PN5b6a6b06369c5812',
    'phone_number':     '5551212',
    'status_url':       'http://anou-cobra-demo.herokuapp.com/communication/sms/status_confirmation',
    'status_secret':    'JuiceIsWorthTheSqueeze',
    'webhook_url':      'http://anou-cobra-demo.herokuapp.com/communication/sms/incoming',
    'webhook_secret':   'QNCWR2444MRT6R2G74UDTMTA6QKM2TET'
  }
else:
  TELERIVET = {
    'api_key':          'DF6UFT49DW643UQWDC436PC2K6LKWEDC',
    'project_id':       'PJ7b2437d72ffb96a200f05f33318f7809',
    'phone_id':         'PNf04607c4af8e227a58457b059a9d583c',
    'phone_number':     '0665555555',
    'status_url':       'http://localcobra.pagekite.me/communication/sms/status_confirmation', #http://respondto.it/anou-sms-status
    'status_secret':    'JuiceIsWorthTheSqueeze',
    'webhook_url':      'http://localcobra.pagekite.me/communication/sms/incoming',
    'webhook_secret':   'QNCWR2444MRT6R2G74UDTMTA6QKM2TET'
  }
if STAGE:
  TELERIVET['status_url'] = 'http://anou-cobra-stage.herokuapp.com/communication/sms/status_confirmation'
  TELERIVET['webhook_url'] = 'http://anou-cobra-stage.herokuapp.com/communication/sms/incoming'
TELERIVET['past_numbers'] = ['212637637566','2120623809088','5551212','0665555555']

#WEPAY PAYMENT AND CHECKOUT PROCESSING
if PAYMENTS_PRODUCTION:
  WEPAY = {
    'client_id':      '114473',
    'client_secret':  '443ad32d57',
    'access_token':   'PRODUCTION_ed41e33671a46b6a3a93e6c6c6d45265fcb62a8f04998d232391bcd3e39749f9',
    'account_id':     '519238566',
    'redirect_uri':   'http://www.theanou.com/checkout/confirmation'
  }
else:
  WEPAY = {
    'client_id':      '137470',
    'client_secret':  '463bfe717b',
    'access_token':   'STAGE_3c234c249310a336d4999b8604b73a27ac5ec6e7255ac9a7ef3d0b6c2629079e',
    'account_id':     '854657449',
    'redirect_uri':   'http://localcobra.pagekite.me/checkout/confirmation'
  }
if STAGE:
  WEPAY['redirect_uri'] = 'http://anou-cobra-stage.herokuapp.com/checkout/confirmation'
if DEMO:
  WEPAY['redirect_uri'] = 'http://anou-cobra-demo.herokuapp.com/checkout/confirmation'

if PRODUCTION or ('CACHEING' in os.environ and os.environ['CACHEING'] == 'ON'):
  CACHES = memcacheify()
else:
  CACHES = {
    'default': {
      'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
  }

DEBUG_TOOLBAR_PANELS = (
  'debug_toolbar.panels.version.VersionDebugPanel',
  'debug_toolbar.panels.timer.TimerDebugPanel',
  'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
  'debug_toolbar.panels.headers.HeaderDebugPanel',
  'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
  'debug_toolbar.panels.template.TemplateDebugPanel',
  'debug_toolbar.panels.sql.SQLDebugPanel',
  'debug_toolbar.panels.signals.SignalDebugPanel',
  'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
  'INTERCEPT_REDIRECTS': False,
  #'HIDE_DJANGO_SQL': False,
  #'TAG': 'div',
  #'ENABLE_STACKTRACES' : True,
}

############## END 3RD PARTY SERVICES ##################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
  'www.theanou.com',
  'anou-cobra.herokuapp.com',
  'anou-cobra-stage.herokuapp.com',
  'anou-cobra-demo.herokuapp.com',
  'localhost'
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Casablanca'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
if PRODUCTION or STAGE or DEMO:
  MEDIA_ROOT = '/media/'
else:
  MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://s3.amazonaws.com/' + AWS_STORAGE_BUCKET_NAME + '/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
AWS_STATIC_URL = 'http://s3.amazonaws.com/' + AWS_STORAGE_BUCKET_NAME + '/'
STATIC_URL = AWS_STATIC_URL
if not (PRODUCTION or STAGE or DEMO): STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
  os.path.join(SITE_ROOT, 'static'),
  ('public', os.path.join(SITE_ROOT, 'apps/public/static')),
  ('seller', os.path.join(SITE_ROOT, 'apps/seller/static')),
  ('admin', os.path.join(SITE_ROOT, 'apps/admin/static')),
  ('communication', os.path.join(SITE_ROOT, 'apps/communication/static')),

  # Put strings here, like "/home/html/static" or "C:/www/django/static".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  #'django.contrib.staticfiles.finders.DefaultStorageFinder',
  'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
if PRODUCTION or STAGE or DEMO:
  SECRET_KEY = 'sx^lszi^cgqdvv#g^djamr56=pkqatt(20=bjeo3++*v8rbue!'
else:
  SECRET_KEY = 'ie+b=mflibb8_#tzf_3&amp;+l$@=kgbgapj-8odui3b&amp;18a(c!$vz'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
# 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  #'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  # Uncomment the next line for simple clickjacking protection:
  # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
if not (PRODUCTION or STAGE or DEMO):
  MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = 'settings.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'settings.wsgi.application'

TEMPLATE_DIRS = (
  os.path.join(SITE_ROOT, 'templates'),
  os.path.join(SITE_ROOT, 'templates/errors'),
  # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
)
if not (PRODUCTION or STAGE or DEMO):
  TEMPLATE_DIRS += ('C:\django\django-debug-toolbar\debug_toolbar\templates',)

INSTALLED_APPS = (
  'apps.public',
  'apps.seller',
  'apps.admin',
  'apps.communication',
  #'api',
  #'djrill',
  'storages',
  #'compressor',
  'south',
  #'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.sitemaps',
  # Uncomment the next line to enable the admin:
  #'django.contrib.admin',
  # Uncomment the next line to enable admin documentation:
  # 'django.contrib.admindocs',
)
if not (PRODUCTION or STAGE or DEMO):
  INSTALLED_APPS += ('debug_toolbar',)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  #'django.contrib.auth.context_processors.auth',
  'django.contrib.messages.context_processors.messages',
  'django.core.context_processors.request',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.RequireDebugFalse'
    }
  },
  'handlers': {
    'mail_admins': {
      'level': 'ERROR',
      'filters': ['require_debug_false'],
      'class': 'django.utils.log.AdminEmailHandler'
    }
  },
  'loggers': {
    'django.request': {
      'handlers': ['mail_admins'],
      'level': 'ERROR',
      'propagate': True,
    },
  }
}
