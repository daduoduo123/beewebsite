from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from blog.models import Blog
from read_statistics.utils import get_today_hot_data, get_seven_days_read_data, get_yesterday_hot_data, \
    get_7_days_hot_blogs, get_30_days_hot_blogs


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天，30天热门博客的缓存视频
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)

    hot_blogs_for_30_days = cache.get('hot_blogs_for_30_days')
    if hot_blogs_for_30_days is None:
        hot_blogs_for_30_days = get_30_days_hot_blogs()
        cache.set('hot_blogs_for_30_days', hot_blogs_for_30_days, 3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    context['hot_blogs_for_30_days'] = hot_blogs_for_30_days
    return render(request, 'home.html', context)
