from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^content/', include('readmore.content.urls')),
    url(r'^widgets/', include('readmore.widgets.urls')),
    url(r'^teacher/', include('readmore.teacher.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^', include('readmore.main.urls')),
)
