import json

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from provider.oauth2.models import AccessToken


def _get_access_token(request):
    token = request.GET.get('access_token')

    try:
        access_token = AccessToken.objects.get_token(token)
    except AccessToken.DoesNotExist:
        raise PermissionDenied

    return access_token


def user(request):
    access_token = _get_access_token(request)
    base_url = 'http://%s' % request.get_host()
    data = access_token.user.get_api_dict(base_url)
    return HttpResponse(json.dumps(data), content_type='application/json')


def minecraft_accounts(request):
    access_token = _get_access_token(request)
    base_url = 'http://%s' % request.get_host()
    minecraft_accounts = access_token.user.minecraft_accounts.all()
    data = [account.get_api_dict(base_url) for account in minecraft_accounts]
    return HttpResponse(json.dumps(data), content_type='application/json')
