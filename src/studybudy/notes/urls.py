from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = 'notes'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload_notes/$', views.upload_notes, name='upload_notes'),
    url(r'^new_folder/$', views.create_newFolder, name='create_new_folder'),
    url(r'^new_file/$', views.create_newFile, name='create_new_file'),
    url(r'^rename_file/$', views.rename_File, name='rename_file'),
    url(r'^details/$', views.get_details, name='details'),
    url(r'^change_description/$', views.change_description, name='change_description'),
    url(r'^make_public/$', views.make_public, name='ajax_change_public'),
    url(r'^star_file/$', views.star_file, name='star_file'),
    url(r'^share_file/$', views.share_file, name='ajax_share_file'),
    url(r'^open_file/$', views.open_file, name='open_file'),
    url(r'^(?P<file_id>[0-9]+)/open_File/$', views.open_File, name='open_file_new_tab'),
    url(r'^save_file/$', views.save_file, name='save_file'),
    url(r'^delete_file/$', views.delete_file, name='delete_file'),
    url(r'^quiz_note/$', views.quiz_note, name='quiz_note'),
    url(r'^summarize/$', views.summarize, name='summarize'),
    url(r'^quiz_result/$', views.quiz_result, name='quiz_result'),
    url(r'^move_list/$', views.move_list, name='move_list'),
    url(r'^move/$', views.move, name='move'),
    url(r'^(?P<file_id>[0-9]+)/download_file/$', views.download_file, name='download_file'),
    url(r'^filter_note/$', views.filter_note, name='filter_note'),
    url(r'^(?P<order_id>[a-z]+)/order_note/$', views.order_note, name='order_note'),
    # re_path(r'^order_note/(?P<order>[a-z]{4})/(?P<file_type>[a-z]{2})/$', views.order_note, name='order_note'),
    url(r'^(?P<view_id>[a-z]+)/change_view/$', views.change_view, name='change_view'),
    url(r'^stared_note/$', views.stared, name='stared_note'),
    url(r'^shared_note/$', views.shared, name='shared_note'),
    url(r'^(?P<folder_id>[0-9]+)/folder_content/$', views.folder_content, name='folder_content'),
]