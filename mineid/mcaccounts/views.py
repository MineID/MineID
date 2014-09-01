from django.views.generic import ListView, FormView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, resolve_url

from braces.views import LoginRequiredMixin

from .models import MinecraftAccount
from .forms import MinecraftAccountForm


class MinecraftViewMixin(LoginRequiredMixin):
    pass


class MinecraftList(MinecraftViewMixin, ListView):
    template_name = 'mineid/mcaccounts/list.html'

    def get_queryset(self):
        return MinecraftAccount.objects.filter(user=self.request.user)


class MinecraftCreate(MinecraftViewMixin, FormView):
    form_class = MinecraftAccountForm
    template_name = 'mineid/mcaccounts/create.html'
    success_url = reverse_lazy('minecraft:list')

    def form_valid(self, form):
        form.save(self.request.user)
        return redirect(self.get_success_url())


class MinecraftDelete(MinecraftViewMixin, DeleteView):
    model = MinecraftAccount
    template_name = 'mineid/mcaccounts/delete.html'
    success_url = reverse_lazy('minecraft:list')
