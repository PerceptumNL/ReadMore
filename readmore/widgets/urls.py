from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'dummy/?$', 'readmore.widgets.dummy.views.process',
        name='widget_dummy'),
    url(r'carddeck/?$', 'readmore.widgets.views.carddeck',
        name='widget_carddeck_test'),
    url(r'dictionary/?$', 'readmore.widgets.dictionary.views.process',
        name='widget_dictionary'),
    url(r'askteacher/?$', 'readmore.widgets.askteacher.views.process',
        name='widget_askteacher'),
    url(r'customcard/?$', 'readmore.widgets.customcard.views.process',
        name='widget_customcard'),
    url(r'seemore/', 'readmore.widgets.seemore.views.process',
    	name='widget_seemore'))

