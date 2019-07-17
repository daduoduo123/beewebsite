from django.contrib import admin
from .models import Blog, BlogType, Tag


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'c_time', 'blog_type']


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
