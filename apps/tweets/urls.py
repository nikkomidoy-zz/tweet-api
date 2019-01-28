
from django.urls import path

from .views import UserTweetAPIView


urlpatterns = [
    path('<slug:screen_name>/', UserTweetAPIView.as_view(), name='users'),
]
