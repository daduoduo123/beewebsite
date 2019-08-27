from urllib.parse import urlencode
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_login_qq_url():
    params = {
        'response_type': 'code',
        'client_id': settings.QQ_APP_ID,  # qq的appid
        'redirect_url': settings.QQ_REDIRECT_URL,
        'state': settings.QQ_STATE,
    }
    return 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)


@register.simple_tag()
def get_login_weixin_url():
    params = {
        'appid': settings.WX_APP_ID,
        'redirect_uri': settings.WX_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'snsapi_login',
        'state': settings.WX_STATE
    }
    return 'https://open.weixin.qq.com/connect/qrconnect?' + urlencode(params)


@register.simple_tag()
def get_login_weibo_url():
    params = {
        'client_id': settings.WB_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': settings.WB_REDIRECT_URI,
    }
    return 'https://api.weibo.com/oauth2/authorize?' + urlencode(params)
