from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('mineid.core.urls')),
    url(r'^accounts/', include('mineid.accounts.urls')),
    url(r'^apps/', include('mineid.apps.urls', namespace='app')),
    #url(r'^minecraft/', include('mineid.mcaccounts.urls',
    #    namespace='minecraft')),
    url(r'^oauth/', include('mineid.oauth.urls', namespace='oauth2')),
    url(r'^api/', include('mineid.api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
