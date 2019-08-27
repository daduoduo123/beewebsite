from django.urls import path
from . import views
from .feeds import ALLBlogRssFeed

# 应用命名空间
app_name = 'blog'
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
    path('tag/<int:blog_tag_pk>', views.blogs_with_tag, name='blogs_with_tag'),
    path('rss/', ALLBlogRssFeed(), name='rss'),  # RSS订阅
]
