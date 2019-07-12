"""beewebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # 加载图片路由
    path('blog/', include('blog.urls')),  # 博客路由分发
    path('comment/', include('comment.urls')),  # 评论路由分发
    path('login/', include('login.urls')),  # 登录注册路由分发
    path('likes/', include('likes.urls')),  # 点赞路由分发
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
