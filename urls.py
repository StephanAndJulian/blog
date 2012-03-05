from django.conf.urls.defaults import patterns, include, url
from webblog.views import *

# Uncomment the next two lines to enable the admin:'blog.views.home', name='home'
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^index/post=(?P<postnumber>\d+)[/]?$',index),
     url(r'^index.*$', redirect_index),
     url(r'^login[/]?$', login),
     url(r'^register[/]?$', register),
     url(r'^blogpost/new[/]?$', create_blogpost),
     url(r'^blogpost/edit/id=(?P<postid>\d+)[/]?$', edit_blogpost),
     url(r'^blogpost/delete/id=(?P<postid>\d+)[/]?$', delete_blogpost),
     url(r'^blogpost/detail/id=(?P<postid>\d+)[/]?$', detail_blogpost),
     url(r'^logout/$', logout)
    # url(r'^blog/', include('blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
