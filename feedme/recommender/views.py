from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext

from GoogleReader import GoogleReader

from recommender.forms import RecommendForm, GoogleLoginForm
from recommender.postrank import PostRank


def landing(request):
    """
    Renders a landing page
    """
    return render_to_response("recommender/landing.html", {
        "recommend_form": RecommendForm(),
        "google_form": GoogleLoginForm(),
    }, context_instance=RequestContext(request))


def recommend_with_url(request):
    """
    Make a recommendation from a single URL
    """
    form = RecommendForm(request.POST)

    if form.is_valid():
        client = PostRank()
        feed_hash = client.get_feed_hash(form.cleaned_data.get("url"))
        recommendations = client.get_recommendations([feed_hash], limit=5)

        if recommendations:
            if request.is_ajax():
                template = "results.html"
            else:
                template = "results_page.html"

            return render_to_response("recommender/%s" % template, {
                "results": recommendations,
            }, context_instance=RequestContext(request))

    return render_to_response("recommender/url.html", {
        "recommend_form": form,
    }, context_instance=RequestContext(request))


def recommend_with_google(request):
    """
    Make a recommendation by parsing the user's google reader feeds
    """
    form = GoogleLoginForm(request.POST)

    if form.is_valid():
        cache_key = "feed-hashes-%s" % form.cleaned_data.get("username")
        feed_hashes = cache.get(cache_key)
        
        if not feed_hashes:
            reader = GoogleReader()
            reader.identify(form.cleaned_data.get("username"), form.cleaned_data.get("password"))

            if reader.login():
                feeds = reader.get_subscription_list()
                client = PostRank()
                feed_hashes = []

                for feed in feeds.get("subscriptions"):
                    if feed.get("id"):
                        feed_hash = client.get_feed_hash(feed.get("id")[5:])

                        if feed_hash:
                            feed_hashes.append(feed_hash)

                cache.set(cache_key, feed_hashes, 24 * 60 * 60)
            else:
                if request.is_ajax():
                    template = "google_error.html"
                else:
                    template = "google_error_page.html"

                return render_to_response("recommender/%s" % template, {

                }, context_instance=RequestContext(request))

        if feed_hashes:
            recommendations = client.get_recommendations(feed_hashes, limit=5)

            if recommendations:
                if request.is_ajax():
                    template = "results.html"
                else:
                    template = "results_page.html"

                return render_to_response("recommender/%s" % template, {
                    "results": recommendations,
                }, context_instance=RequestContext(request))

    return render_to_response("recommender/google.html", {
        "recommend_form": form,
    }, context_instance=RequestContext(request))
