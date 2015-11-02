from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^students/process/$', views.process_students),
    url(r'^students/$', views.student_form, name='student_form'),
    url(r'^teachers/process/$', views.process_teachers),
    url(r'^teachers/$', views.teacher_form, name='teacher_form'),
]

