from django.conf.urls import url
from . import views

app_name = 'quiz'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^save_quiz/$', views.save_quiz, name='save_quiz'),
    url(r'^(?P<file_id>[0-9]+)/quiz_attempt/$', views.quiz_attempt, name='quiz_attempt'),
]