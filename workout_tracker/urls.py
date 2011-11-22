from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^register/geoloqi$',
        'core.views.register',
        name='core_register'),

    url(r'^register/geoloqi-callback$',
        'core.views.register_callback',
        name='core_register_callback'),

    # url(r'^workout_tracker/', include('workout_tracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)