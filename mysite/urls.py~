from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    (r'^$', 'lzc.views.blog'),
    (r'^log/$', 'lzc.views.log'),
    (r'^log_success/$', 'lzc.views.log_success'),
    (r'^homepage/$', 'lzc.views.homepage'),
    (r'^users/$', 'lzc.views.users'),
    (r'^posts/([0-9]+)/$', 'lzc.views.posts'),
    (r'^homepage/retrieve/$', 'lzc.views.retrieve'),
    (r'^homepage/release/$', 'lzc.views.release') 
    #(r'^admin/', include(admin.site.urls)),
) 
