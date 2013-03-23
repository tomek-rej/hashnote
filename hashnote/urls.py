from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hashnote.views.home', name='home'),
    # url(r'^hashnote/', include('hashnote.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^hashnote_ui/add_note', 'hashnote_ui.views.add_note'),
    url(r'^hashnote_ui/', 'hashnote_ui.views.index'),
)

urlpatterns += staticfiles_urlpatterns()