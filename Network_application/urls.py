from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Network_application.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Network_application.view.network'),
    url(r'^test/$', 'Network_application.view.network_test'),
    url(r'^openvpn/$', 'Network_application.view.openvpn'),
    url(r'^queren/(.*?)$', 'Network_application.view.queren'),
    url(r'^ok/$', 'Network_application.view.ok'),
    url(r'^404/$', 'Network_application.view.error_404'),
    url(r'^index/$','Network_application.view.index'),
    url(r'^login/$','Network_application.login.login'),
    url(r'^logout/$','Network_application.login.logout'),
)
