from urlparse import urlparse

from django.utils.translation import ugettext as _

from provider.oauth2.forms import AuthorizationRequestForm
from provider.forms import OAuthValidationError


class AuthorizationRequestForm(AuthorizationRequestForm):
    def clean_redirect_uri(self):
        """
        Change original behavior to accept variable redirect_uri's
        """
        redirect_uri = self.cleaned_data.get('redirect_uri')

        if redirect_uri:
            if not self.domain_cmp(redirect_uri, self.client.redirect_uri):
                raise OAuthValidationError({
                    'error': 'invalid_request',
                    'error_description': _("The requested redirect didn't "
                        "match the client settings.")})

        return redirect_uri

    def domain_cmp(self, redirect_uri, client_redirect_uri):
        """ Returns if redirect_uri has the same domain or it is a
            subdomain of client_redirect_uri.
        """
        redirect_domain = urlparse(redirect_uri).hostname
        client_domain = urlparse(client_redirect_uri).hostname

        return redirect_domain.endswith(client_domain)
