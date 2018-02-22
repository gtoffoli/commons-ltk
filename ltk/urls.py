"""ltk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(r'^regexp/$', views.Regexp.as_view(), name="regexp"),
    re_path(r'^language/(?P<language_code>[\w-]*)/set/$', views.language, name="language"),
    re_path(r'^$', views.home, name="home"),
]

urlpatterns += [
    # url (r'^accounts/signup/$', views.signup, name='account_signup'), # 131015 GT
    # url (r'^accounts/', include('allauth.urls')),
    re_path(r'^accounts/profile/', TemplateView.as_view(template_name='account/profile.html'), name='welcome',),
]   
