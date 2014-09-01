from django.conf.urls import patterns, include, url

from .views import AppList, AppCreate, AppUpdate, AppDelete, AppCredentials

urlpatterns = patterns(
    '',
    url(r'^$', AppList.as_view(), name='list'),
    url(r'^create/$', AppCreate.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', AppUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', AppDelete.as_view(), name='delete'),
    url(r'^credentials/(?P<pk>\d+)/$', AppCredentials.as_view(),
        name='credentials'),
)
