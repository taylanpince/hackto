from django import forms
from django.utils.translation import ugettext_lazy as _


class RecommendForm(forms.Form):
    """
    A form for getting a single domain for a recommendation
    """
    url = forms.URLField(label=_("URL"), verify_exists=True, initial="huffingtonpost.com")


class GoogleLoginForm(forms.Form):
    """
    A form for getting the user's Google credentials
    """
    username = forms.CharField(label=_("Email"), initial="email")
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, initial="password")
