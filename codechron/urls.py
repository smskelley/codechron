from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from blog.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', BlogHome.as_view(), name='Home'),
    url(r'^$', BlogHome.as_view(), name='Home'),
    url(r'^archive/$', BlogArchive.as_view(), name='Archive'),
    url(r'^about/$', BlogAbout.as_view(), name='About'),
    url(r'^post/(?P<PostId>\d+)/$', BlogViewPost.as_view(), name='ViewPost'),
    url(r'^comments/(?P<PostId>\d+)$', BlogAjaxComments.as_view(), name='AjaxComments'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name = 'robots.txt')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
