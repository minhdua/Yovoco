"""yovoco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
		. Add an import: from my_app import views
	2. Add a URL to urlpatterns: path(VALUE_EMPTY_STRING, views.home, name='home')
Class-based views
		. Add an import: from other_app.views import Home
	2. Add a URL to urlpatterns: path(VALUE_EMPTY_STRING, Home.as_view(), name='home')
Including another URLconf
		. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from yovoco.views import language_list, part_of_speech_list, quiz_type_list

urlpatterns=[
	path('admin/', admin.site.urls, name='admin'),
	path(settings.BASE_URL, include('entities.urls'),name='entities'),
	path(settings.BASE_URL + "user/", include('users.urls'),name='user'),
	path(settings.BASE_URL + "study/", include('study.urls'),name='study'),
	path(settings.BASE_URL + "common/languages/", language_list, name='languages'),
	path(settings.BASE_URL + "common/poses/", part_of_speech_list, name='poses'),
	path(settings.BASE_URL + "common/qtypes/", quiz_type_list, name='qtypes'),
]
