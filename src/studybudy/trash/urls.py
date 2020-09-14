from django.conf.urls import url
from . import views

app_name = 'trash'

urlpatterns = [
    url(r'^$', views.trash, name='trash'),
    url(r'^recycle_list/$', views.recycle_list, name='recycle_list'),
    url(r'^recycle/$', views.recycle, name='recycle'),
    url(r'^delete_permanently', views.delete_permanently, name='delete_permanently'),
    url(r'^details/$', views.get_details, name='details'),

]