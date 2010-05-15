import httplib

from urllib import urlencode

from django.conf import settings
from django.utils import simplejson


GOOGLE_READER_SERVER = "www.google.com"
GOOGLE_READER_API_URL = "http://%s/reader/api/0"
GOOGLE_READER_AUTH_URL = "https://www.google.com/accounts/ClientLogin"
GOOGLE_READER_CLIENT = getattr(settings, "GOOGLE_READER_CLIENT", "default")


class GoogleReader(object):
    """
    Google Reader client for making API requests
    """
    def __init__(self):
        super(GoogleReader, self).__init__()

        self.connection = httplib.HTTPConnection(GOOGLE_READER_SERVER)
        self.session_id = None

    def authenticate(self, username, password):
        """
        Get an auth token for the client
        """
        secure_connection = httplib.HTTPSConnection(GOOGLE_READER_SERVER)
        body = urlencode({
            "service": "reader",
            "Email": username,
            "Passwd": password,
            "source": GOOGLE_READER_CLIENT,
            "continue": "http://www.google.com/",
        })
        print body
        secure_connection.request("POST", GOOGLE_READER_AUTH_URL, body, {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
        })

        response = secure_connection.getresponse()
        payload = response.read()
        print payload
        

    def fetch(self, path, params={}):
        """
        Make the actual request
        """
        params.update({
            "format": "json",
            "client": GOOGLE_READER_CLIENT,
            "ck": time.mktime(datetime.now().timetuple())
        })

        self.connection.request("GET", "%(url)s%(path)s?%(query)s" % {
            "url": GOOGLE_READER_API_URL,
            "path": path,
            "query": urlencode(params),
        }, None, {
            "Cookie": "SID: %s" % self.session_id,
        })

        response = self.connection.getresponse()
        payload = response.read()

        return simplejson.loads(payload)

    def get_subscription_list(self):
        """
        Return a list of feeds the user is subscribed to
        """
        response = self.fetch("/subscription/list")

        return response
