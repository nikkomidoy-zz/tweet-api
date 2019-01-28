import coreapi
import coreschema

from rest_framework import (
    permissions,
    status,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from . import tweet_api


class UserTweetAPIView(APIView):
    """
    A simple APIView for getting user tweet data
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "screen_name",
            required=True,
            location="path",
            schema=coreschema.String(
                title="screen_name",
                description="Name of a specific user to search for tweets.",
            )
        ),
        coreapi.Field(
            "limit",
            required=False,
            location="query",
            schema=coreschema.String(
                title="limit",
                description="Define result count",
            )
        ),
    ])
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            screen_name = kwargs.get('screen_name')
            limit = request.GET.get('limit', 30)
            results = tweet_api.fetch_user_tweets_data(
                screen_name,
                limit,
            )
            return Response(
                results,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {'error': "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
