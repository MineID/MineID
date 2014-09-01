from django.views.generic import TemplateView
from django.shortcuts import redirect


class Home(TemplateView):
    template_name = 'mineid/core/home.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('app:list')
        return super(Home, self).get(request)
