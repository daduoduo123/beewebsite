from django.urls import path
from . import views

app_name = 'my_notifications'
urlpatterns =[
    path('', views.my_notifications, name='my_notifications'),
    path('<int:my_notification_pk>', views.my_notification, name='my_notification'),
    path('delete_my_read_notification/', views.delete_my_read_notifications, name='delete_my_read_notifications'),
]