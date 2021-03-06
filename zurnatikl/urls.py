from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from ajax_select import urls as ajax_select_urls


admin.autodiscover()


urlpatterns = [
    url(r'^', include('zurnatikl.apps.content.urls')),
    # TODO: eventually, move about/credit page templates into content
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),
        name='about'),
    url(r'^credits/$', TemplateView.as_view(template_name="credits.html"),
        name='credits'),
    url(r'^legal/$', TemplateView.as_view(template_name="legal.html"),
        name='legal'),
    url(r'^network/', include('zurnatikl.apps.network.urls',
        namespace='network')),
    url(r'^journals/', include('zurnatikl.apps.journals.urls',
        namespace='journals')),
    url(r'^people/', include('zurnatikl.apps.people.urls',
        namespace='people')),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls) ),

    # add redirect for favicon at root of site
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
