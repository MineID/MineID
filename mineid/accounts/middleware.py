from urllib import quote

from django.http import QueryDict
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect


ALLOWED_URLS = (
    reverse_lazy('set_email_address'),
    reverse_lazy('logout'),
)


class RequireEmailMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.email:
            urls = [str(url) for url in ALLOWED_URLS]
            skip = any(request.path.startswith(url) for url in urls)
            if not skip:
                # /oauth/authorize
                path = request.path
                # response_type=code&redirect_uri=/foo/ 
                qs = request.GET.urlencode()

                # /set_email_address?next=/oauth/authorize?response_code=...
                redir = urls[0] + '?next=' + path + quote('?' + qs)

                return redirect(redir)
