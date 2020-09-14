from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^change/$', views.change, name='change'),
    url(r'^(?P<user_id>[0-9]+)/edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^(?P<user_id>[0-9]+)/delete_image/$', views.delete_image, name='delete_image'),
    
]