from django.conf.urls import patterns, include, url

from .views import MinecraftList, MinecraftCreate, MinecraftDelete

urlpatterns = patterns(
    '',
    url(r'^$', MinecraftList.as_view(), name='list'),
    url(r'^create/$', MinecraftCreate.as_view(), name='create'),
    url(r'^delete/(?P<pk>\d+)/$', MinecraftDelete.as_view(), name='delete'),
)
