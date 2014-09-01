from django.conf.urls import patterns, include, url

from .views import user, minecraft_accounts

urlpatterns = patterns(
    '',
    url(r'^user$', user, name='user'),
    url(r'^minecraft_accounts$', minecraft_accounts,
        name='minecraft_accounts'),
)
