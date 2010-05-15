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
        print feed_hash
        print recommendations
        if recommendations:
            return render_to_response("recommender/results.html", {
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
        reader = GoogleReader()
        reader.identify(form.cleaned_data.get("username"), form.cleaned_data.get("password"))

        if reader.login():
            feeds = reader.get_subscription_list()
            client = PostRank()
            feed_hashes = []

            for feed in feeds.get("subscriptions"):
                feed_hashes.append(client.get_feed_hash(feed.get("id")))
            print feed_hashes
            recommendations = client.get_recommendations(feed_hashes, limit=5)
            print recommendations
            if recommendations:
                return render_to_response("recommender/results.html", {
                    "results": recommendations,
                }, context_instance=RequestContext(request))

    return render_to_response("recommender/google.html", {
        "recommend_form": form,
    }, context_instance=RequestContext(request))
