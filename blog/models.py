from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

from read_statistics.models import ReadNumExpandMethod, ReadDetail


# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=64,verbose_name='博客类型')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '博客类型'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=16, verbose_name='标签名')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=64,verbose_name='标题')
    content = RichTextUploadingField(verbose_name='内容')
    c_time = models.DateTimeField(auto_now_add=False,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    read_detail = GenericRelation(ReadDetail,verbose_name='阅读详情')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    tags = models.ManyToManyField(Tag, blank=True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name='博客类型')

    def __str__(self):
        return self.title

    def get_user(self):
        return self.author

    def get_url(self):
        return reverse('blog:blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    # 固定名称给rss使用
    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'blog_pk': self.pk})

    class Meta:
        ordering = ['-c_time']
        verbose_name = '博客'
        verbose_name_plural = verbose_name
