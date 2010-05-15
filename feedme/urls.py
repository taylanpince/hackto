from django.conf.urls.defaults import *


urlpatterns = patterns('recommender.views',
    url(r'^$', 'landing', name="recommender_landing"),
    url(r'^recommend/$', 'recommend_with_url', name="recommender_url"),
    url(r'^recommend/google/$', 'recommend_with_google', name="recommender_google"),
)
