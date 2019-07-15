from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class OAuthRelationship(models.Model):
    OAUTH_TYPE_CHOICES = (
        (0, 'QQ'),
        (1, 'WeChat'),
        (2, 'Sina'),
        (3, 'Github'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    openid = models.CharField(max_length=128)
    oauth_type = models.IntegerField(choices=OAUTH_TYPE_CHOICES, default=0, verbose_name='第三方登录方式')

    def __str__(self):
        return 'OAuthRelationship:%s' % self.user.username

    class Meta:
        verbose_name = '第三方账号关系'
        verbose_name_plural = verbose_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=24, verbose_name='昵称')

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user)

    class Meta:
        verbose_name = '用户拓展信息'
        verbose_name_plural = '用户拓展信息'


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


def has_nickname(self):
    return Profile.objects.filter(user=self).exists()


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username
