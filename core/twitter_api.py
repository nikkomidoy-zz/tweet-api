import requests

from django.conf import settings
from requests_oauthlib import OAuth1, OAuth2

try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

from .exceptions import RequestError


class TweetApi(object):
    """
    A class object on handling Twitter data
    """
    def __init__(self, base_url=None):

        self.__twitter_auth = None
        self.base_url = base_url or 'https://api.twitter.com/1.1'
        self._session = requests.Session()
        self.auth_dict = dict(
            consumer_key=settings.TWITTER_KEYS.get('consumer_key'),
            consumer_secret=settings.TWITTER_KEYS.get('consumer_secret'),
            access_token_key=settings.TWITTER_KEYS.get('access_token'),
            access_token_secret=settings.TWITTER_KEYS.get('access_token_secret'),
        )
        self.initialize_authentication(**self.auth_dict)

    def initialize_authentication(self,
                       consumer_key,
                       consumer_secret,
                       access_token_key=None,
                       access_token_secret=None):
        """
        Set the consumer_key and consumer_secret for this instance

        Args:
        consumer_key:
            The consumer_key of the twitter account.
        consumer_secret:
            The consumer_secret for the twitter account.
        access_token_key:
            The oAuth access token key value
        access_token_secret:
            The oAuth access token's secret
        """
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token_key = access_token_key
        self._access_token_secret = access_token_secret

        twitter_auth_list = [consumer_key, consumer_secret,
                     access_token_key, access_token_secret]

        if not all(twitter_auth_list):
            raise RequestError('There are missing oAuth credentials.')

        self.__twitter_auth = OAuth1(consumer_key, consumer_secret,
                                 access_token_key, access_token_secret)


    def search_tweets_data(self, query=None, count=30):
        """
        Search all tweets given a specific query
        """
        if not query:
            raise RequestError('Query terms should be provided.')

        url = '{}/search/tweets.json'.format(self.base_url)
        parameters = dict(
            q=query,
            count=count,
            include_entities=True,
        )

        response = self._request_url(url, data=parameters)
        results = self.build_tweet_results(
            response.json().get('statuses',[])
        )

        return results

    def fetch_user_tweets_data(self, screen_name=None, count=30):
        """
        Get user tweets data
        """
        if not screen_name:
            raise RequestError('User name is required.')

        url = '{}/statuses/user_timeline.json'.format(self.base_url)
        parameters = dict(
            screen_name=screen_name,
            count=count,
        )

        response = self._request_url(url, data=parameters)
        results = self.build_tweet_results(response.json())

        return results

    def build_tweet_results(self, statuses):
        """
        Return data based on the specifications
        """
        tweet_results = [
            dict(
                account=dict(
                    fullname=status.get('name'),
                    href=status.get('url'),
                    id=status.get('id'),
                ),
                date=status.get('created_at'),
                hashtags=set(
                    [
                        hashtag.get('text')
                        for hashtag in status.get('entities',{}).get('hashtags',[])
                    ]
                ) or [],
                likes=status.get('favorite_count'),
                replies=status.get('in_reply_to_user_id'),
                retweets=status.get('retweet_count'),
                text=status.get('text'),
            )
            for status in statuses
        ]

        return tweet_results


    def construct_url(self, url, params={}):
        """
        Build URL for requesting url
        """
        get_params = urlencode(params)
        encoded_url = '{}?{}'.format(url, get_params)
        return encoded_url

    def _request_url(self, url, data=None, enforce_auth=True):
        """
        A URL request

        Args:
            url:
                A location to be retrieved

        Returns:
            A JSON object.
        """
        if enforce_auth:
            if not self.__twitter_auth:
                raise RequestError('Authentication credentials must be provided.')


        url = self.construct_url(url, params=data)
        response = self._session.get(url, auth=self.__twitter_auth)

        return response
