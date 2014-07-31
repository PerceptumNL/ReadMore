from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'dummy/?$', 'readmore.widgets.dummy.views.process',
        name='widget_dummy'))
