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
# from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path(r'dashboard', views.dashboard, name="dashboard"),
    path(r'dashboard/<int:year>', views.dashboard, name="dashboard"),
    path(r'upload-file', views.upload_file, name="upload-file"),
    path(r'get-progress', views.upload_file_progress, name="upload-file-progress"),
    path(r'change-data-status', views.change_data_status, name="change-data-status"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += staticfiles_urlpatterns()
