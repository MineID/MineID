from django.core import signing
from django.utils.translation import ugettext as _

from provider.oauth2.views import Authorize

from .forms import AuthorizationRequestForm


class Authorize(Authorize):
    def get_request_form(self, client, data):
        return AuthorizationRequestForm(data, client=client)

    def get_data(self, request, key='params'):
        switch_account = request.COOKIES.get('switch_account')

        if switch_account:
            try:
                data = signing.loads(switch_account)
                self.cache_data(request, data)
                return data
            except signing.BadSignature:
                pass

        return super(Authorize, self).get_data(request, key=key)

    def get(self, request, *args, **kwargs):
        response = super(Authorize, self).get(request, *args, **kwargs)

        if 'switch_account' in request.COOKIES:
            response.delete_cookie('switch_account')

        return response
