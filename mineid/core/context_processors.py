from django.contrib.sites.models import Site


def domain(request):
    return {'domain': request.get_host()}
