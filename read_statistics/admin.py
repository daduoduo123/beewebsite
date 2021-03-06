from django.contrib import admin
from .models import ReadDetail, ReadNum


# Register your models here.

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['read_num', 'content_object']


@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ['read_num', 'date', 'content_object']
