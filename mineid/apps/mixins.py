from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from provider.oauth2.models import Client
from braces.views import LoginRequiredMixin, FormValidMessageMixin

from ..core.mixins import UserObjectsMixin
from .forms import ClientForm


class AppViewMixin(LoginRequiredMixin):
    pass


class AppUserObjectMixin(object):
    model = Client


class AppEditObjectMixin(object):
    success_url = reverse_lazy('app:list')


class AppUserObjectsMixin(AppUserObjectMixin, UserObjectsMixin):
    pass


class BaseAppFormMixin(AppEditObjectMixin):
    form_class = ClientForm

    def form_valid(self, form):
        form.save(self.request.user)
        self.object = form.instance
        return redirect(self.get_success_url())


class AppFormMixin(FormValidMessageMixin, BaseAppFormMixin):
    pass


class AppDeleteMixin(FormValidMessageMixin, AppEditObjectMixin):
    def delete(self, *args, **kwargs):
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        return super(AppDeleteMixin, self).delete(*args, **kwargs)
