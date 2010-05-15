import os
import sys

sys.path.append("/home/taylan/sites/feedme/lib/python2.5/site-packages")
sys.path.append("/home/taylan/sites/feedme/src/hackto")
sys.path.append("/home/taylan/sites/feedme/src/hackto/feedme")

os.environ["DJANGO_SETTINGS_MODULE"] = "feedme.settings"

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
