from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^register/geoloqi$',
        'core.views.register_geoloqi',
        name='core_register_geoloqi'),

    url(r'^register/geoloqi-callback$',
        'core.views.register_geoloqi_callback',
        name='core_register_geoloqi_callback'),

    url(r'^register/dailymile$',
        'core.views.register_dailymile',
        name='core_register_dailymile'),

    url(r'^register/dailymile-callback$',
        'core.views.register_dailymile_callback',
        name='core_register_dailymile_callback'),

    # url(r'^workout_tracker/', include('workout_tracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
