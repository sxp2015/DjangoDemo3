"""DjangoDemo3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

# from django.views.static import serve
from DjangoDemo3 import settings

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
                  path('wechat/', include('wechat.urls'), name='wechat'),
                  path('tasks/', include('tasks.urls'), name='tasks'),
                  path('api/', include('api.urls'), name='api'),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 添加路由让静态文件可以访问写法一
# urlpatterns += [
#     re_path(r'^static/(?P<path>.*)$', serve, {'document_root': 'static'})
# ]
