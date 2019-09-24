"""pricing_gov_sys_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import django
from django.conf.urls import url, re_path
from django.http import HttpResponseRedirect

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^$', lambda r: HttpResponseRedirect('admin/login')),
    path('admin/', include("apps.user.urls")),
    path('visualization/', include("apps.visualization.urls")),
    path('', include("apps.data.urls")),

    url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
]
