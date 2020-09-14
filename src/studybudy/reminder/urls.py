from django.conf.urls import url
from . import views

app_name = 'reminder'

urlpatterns = [
    url(r'^$', views.task_list, name='task_list'),
    url(r'^add_task/$', views.add_task, name='add_task'),
    url(r'^(?P<task_id>[0-9]+)/edit_task/$', views.edit_task, name='edit_task'),
    url(r'^delete_task/$', views.delete_task, name='delete_task'),
    url(r'^complete_task/$', views.complete_task, name='complete_task'),
    # url(r'^add_task/$', AppointmentCreateView.as_view(), name='add_task'),

]