from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.teacher.views.overview', name='overview'),
    url(r'^dashboard$', 'readmore.teacher.views.dashboard', name='dashboard'),
    url(r'^woordkaarten$', 'readmore.teacher.views.word_cards', name='word_cards'),
    url(r'^manage_users$', 'readmore.teacher.views.manage_users', name='manage_users'),
    url(r'^add_user$', 'readmore.teacher.views.add_user', name='add_user'),
    url(r'^add_word$', 'readmore.teacher.views.add_word', name='add_word'),
    url(r'^remove_word$', 'readmore.teacher.views.remove_word', name='remove_word'),
    url(r'^carddeck/overview/?$', 'readmore.teacher.views.carddeck_overview',
        name='dashboard_carddeck_overview'),
    url(r'^carddeck/user/?$', 'readmore.teacher.views.carddeck_user',
        name='dashboard_carddeck_user'),
    url(r'^carddeck/article/?$', 'readmore.teacher.views.carddeck_article',
        name='dashboard_carddeck_article'),
    url(r'^carddeck/word/?$', 'readmore.teacher.views.carddeck_word',
        name='dashboard_carddeck_word'),
    url(r'^lists/userlist/?$',
        'readmore.teacher.views.retrieve_students',
        name='retrieve_students'),
        
    url(r'^overview$', 'readmore.teacher.views.dashboard_test', name='dashboard_test'),
    url(r'^group/(?P<group_id>\w+)$', 'readmore.teacher.views.dashboard_group', name='dashboard_group'),
    url(r'^group/(?P<group_id>\w+)/(?P<student_id>\w+)$', 'readmore.teacher.views.dashboard_student', name='dashboard_student'),
    
    url(r'^api/student/(?P<student_id>\w+)$', 'readmore.teacher.views.api_student', name='api_student'),
    
    url(r'^api/group/(?P<group_id>\w+)$', 'readmore.teacher.views.api_group', name='api_group'),
        
)


