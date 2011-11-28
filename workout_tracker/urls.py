from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(template_name='core/index.html'),
        name='index'),

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

    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'),

    url(r'workout/splash$',
        TemplateView.as_view(template_name='workout/splash.html'),
        name='workout_splash'),

    url(r'^workout/start$',
        'core.views.workout_start',
        name='workout_start'),

    url(r'^workout/end$',
        'core.views.workout_end',
        name='workout_end'),

    # url(r'^workout_tracker/', include('workout_tracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
