from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', include('content.urls')),
    url(r'^content/', include('content.urls')),
    url(r'^cover/', include('cover.urls')),
    url(r'^teacher/', include('teacher.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^load_data/', include('load_students.urls')),
    url(r'^', include('main.urls')),
)
