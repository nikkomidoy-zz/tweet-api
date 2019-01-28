
from django.urls import path

from .views import HashtagAPIView


urlpatterns = [
    path('<slug:query>/', HashtagAPIView.as_view(), name='hashtags'),
]
