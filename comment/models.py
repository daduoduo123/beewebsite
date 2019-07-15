

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User



class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField('评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论者')

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE, verbose_name='评论根对象')
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE, verbose_name='评论父对象')
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE, verbose_name='被评论者')

    def __str__(self):
        return self.text

    def get_user(self):
        return self.user

    def get_url(self):
        return self.content_object.get_url()

    class Meta:
        ordering = ['-comment_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name