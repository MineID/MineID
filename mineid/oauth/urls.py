from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from provider.compat.urls import *
from provider.oauth2.views import Redirect, Capture, AccessTokenView
from .views import Authorize


urlpatterns = patterns('',
    url('^authorize/?$',
        login_required(Capture.as_view()),
        name='capture'),
    url('^authorize/confirm/?$',
        login_required(Authorize.as_view()),
        name='authorize'),
    url('^redirect/?$',
        login_required(Redirect.as_view()),
        name='redirect'),
    url('^access_token/?$',
        csrf_exempt(AccessTokenView.as_view()),
        name='access_token'),
)
