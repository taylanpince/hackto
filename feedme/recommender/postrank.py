import httplib

from urllib import urlencode

from django.conf import settings
from django.utils import simplejson


POSTRANK_SERVER = "api.postrank.com"
POSTRANK_API_URL = "http://%s/v2" % POSTRANK_SERVER
POSTRANK_APP_KEY = getattr(settings, "POSTRANK_APP_KEY", "default")


class PostRank(object):
    """
    PostRank client for making API requests
    """
    def __init__(self):
        super(PostRank, self).__init__()

        self.connection = httplib.HTTPConnection(POSTRANK_SERVER)

    def fetch(self, path, params, method="GET", body=None):
        """
        Make the actual request
        """
        params.update({
            "format": "json",
            "appkey": POSTRANK_APP_KEY,
        })

        self.connection.request(method, "%(url)s%(path)s?%(query)s" % {
            "url": POSTRANK_API_URL,
            "path": path,
            "query": urlencode(params),
        }, body)

        response = self.connection.getresponse()
        payload = response.read()

        return simplejson.loads(payload)

    def encode_feed_hashes(self, params):
        """
        Build POST body data from a list of parameters
        """
        body = ""

        for p in params:
            body += "feed[]=%s&" % p

        return body

    def get_feed_hash(self, url):
        """
        Return PostRank feed hash for a feed url
        """
        response = self.fetch("/feed/info", {
            "id": url,
        })

        return response.get("id", None)

    def get_recommendations(self, hashes, limit=5):
        """
        Get PostRank recommendations using a number of feeds
        """
        response = self.fetch("/recommend", {
            "num": limit,
        }, method="POST", body=self.encode_feed_hashes(hashes))

        return response
