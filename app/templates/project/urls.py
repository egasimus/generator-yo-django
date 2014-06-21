from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.cache import cache_page


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin_site.urls), name='admin'),
    url(r'^$', cached(cms.views.HomepageView.as_view()), name='index'))


if settings.SERVE_STATIC:  # defaults to DEBUG
    from django.conf.urls import static
    urlpatterns += static.static(settings.STATIC_URL)
    urlpatterns += static.static(settings.MEDIA_URL,
                                 document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)))
