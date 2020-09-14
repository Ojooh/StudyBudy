"""studybudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from .views import login_page, register_page, login_user, register_user, logout_user
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
 


app_name = 'studybudy'





urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login_page, name='login_page'),
    url(r'^login_user/$', login_user, name='login_user'),
    url(r'^Register/$', register_page, name='register_page'),
    url(r'^register_user/$', register_user, name='register_user'),
    url(r'^logout/$', logout_user, name='logout_user'),
    url(r'^Dashboard/', include('notes.urls')),
    url(r'^Trash/', include('trash.urls')),
    url(r'^Quiz/', include('quiz.urls')),
    url(r'^User/', include('users.urls')), 
    url(r'^Reminder/', include('reminder.urls'))  
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
