import os, sys, urlparse

DATABASES = {}
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('mysql')
try:
    print 'hai1'
    if os.environ.has_key('DATABASE_URL'):
        print 'hai2'
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        print 'hai3'
        DATABASES['default'] = {
            'NAME':     url.path[1:],
            'USER':     url.username,
            'PASSWORD': url.password,
            'HOST':     url.hostname,
            'PORT':     url.port,
        }
        print 'hai4'
        if url.scheme == 'postgres':
            DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
            print 'hai5'
        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
            print 'hai6'
except:
    print 'FAIL'
