import urllib

from django.contrib.sites.models import RequestSite, Site

from django.http import QueryDict
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView, TemplateView, RedirectView
from django.utils.http import is_safe_url
from django.shortcuts import redirect

from django.core.urlresolvers import reverse
from django.core import signing

from registration import signals
from registration.backends.default.views import RegistrationView
from registration.models import RegistrationProfile

from provider.views import Mixin as ProviderMixin

from braces.views import LoginRequiredMixin

from .forms import RegistrationFormUniqueEmail, EmailAddressForm


User = get_user_model()


class RegistrationView(RegistrationView):
    """ Since we don't use usernames (only email addresses), we had
        to inherit this view to remove the username dependency.
    """
    form_class = RegistrationFormUniqueEmail

    def get_context_data(self, **kwargs):
        ctx = super(RegistrationView, self).get_context_data(**kwargs)
        ctx['next'] = self.request.GET.get('next', '')
        return ctx

    def get_success_url(self, request, user):
        next_ = self.request.GET.get('next')
        if next_ and not is_safe_url(url=next_, host=self.request.get_host()):
            next_ = None
        url = reverse('registration_complete')
        if next_:
            url += '?next=' + urllib.quote(next_)
        return url


class RegistrationComplete(TemplateView):
    template_name = 'registration/registration_complete.html'

    def get_context_data(self, **kwargs):
        ctx = super(RegistrationComplete, self).get_context_data(**kwargs)
        ctx['next'] = self.request.GET.get('next', '')
        return ctx


class SetEmailAddress(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EmailAddressForm
    template_name = 'mineid/accounts/set_email_address.html'

    def get(self, request, *args, **kwargs):
        if request.user.email:
            return redirect(self.get_success_url())
        return super(SetEmailAddress, self).get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super(SetEmailAddress, self).get_context_data(**kwargs)
        ctx['next'] = self.request.GET.get('next', '')
        return ctx

    def get_success_url(self):
        next_ = self.request.GET.get('next')
        if next_ and not is_safe_url(url=next_, host=self.request.get_host()):
            next_ = None
        return next_ or '/'


class SwitchAccount(ProviderMixin, RedirectView):
    def get_redirect_url(self):
        next_ = self.request.GET.get('next') or '/'
        return reverse('auth_login') + '?next=' + urllib.quote(next_)

    def get(self, *args, **kwargs):
        data = signing.dumps(self.get_data(self.request))

        response = super(SwitchAccount, self).get(*args, **kwargs)
        response.set_cookie('switch_account', data)

        return response
