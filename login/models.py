from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=24, verbose_name='昵称')

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user)

    class Meta:
        verbose_name='个人简介'
        verbose_name_plural='个人简介'

def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile =Profile.objects.get(user=self)
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

