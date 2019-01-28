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


class HashtagAPIView(APIView):
    """
    A simple APIView for querying hashtags
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "query",
            required=True,
            location="path",
            schema=coreschema.String(
                title="query",
                description="Query string to search for tweets.",
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
            query = kwargs.get('query')
            limit = request.GET.get('limit', 30)
            results = tweet_api.search_tweets_data(
                query,
                limit,
            )
            return Response(
                results,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
