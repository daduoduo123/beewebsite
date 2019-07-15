from notifications.signals import notify
from django.db.models.signals import post_save
from django.utils.html import strip_tags
from django.dispatch import receiver

from .models import LikeRecord


# 当执行save（）方法时会，调到这里执行，有signals监听
@receiver(post_save, sender=LikeRecord)
def send_notification(sender, instance, **kwargs):
    # 发送站内消息
    if instance.content_type.model == 'blog':
        verb = '{0}点赞了你的<<{1}>>'.format(instance.user.get_nickname_or_username(), instance.content_object.title)
    elif instance.content_type.model =='comment':
        verb = '{0}点赞了你的评论"{1}"'.format(instance.user.get_nickname_or_username(), strip_tags(instance.content_object.text))

    recipient = instance.content_object.get_user()
    url = instance.content_object.get_url()
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)

