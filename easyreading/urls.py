#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from reader.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
   
    url(r'^$', 'reader.views.book_list', name='book_list'),
    url(r'^book/(?P<id>(\d+))/$', 'reader.views.book_show', name='book_show'),
    url(r'^category/(?P<id>(\d+))/$','reader.views.category', name='book_category'),
    url(r'^author/(?P<id>(\d+))/$', 'reader.views.author', name='book_author'),

    url(r'^search/', 'reader.views.search', name='search'),

    url(r'^user/login/$', 'reader.views.user_login', name='user_login'),
    url(r'user/logout/$', 'reader.views.user_logout', name='user_logout'),
    url(r'user/register/$', 'reader.views.register', name='register'),
    
    url(r'^book/read/(?P<id>(\d+))/$', 'reader.views.read', name='read'),
    url(r'^book/chapter/(?P<id>(\d+))/$', 'reader.views.read_page', name='read_page'),
    url(r'^book/chapters/(?P<id>(\d+))/$', 'reader.views.get_next_content', name='get_next_content'),
    url(r'^book/contents/list/(?P<id>(\d+))/$', 'reader.views.get_content_list', name='get_content_list'),

    url(r'^user/collect/(?P<id>(\d+))/$', 'reader.views.collect', name='collect'),
    url(r'^user/discollect/(?P<id>(\d+))/$', 'reader.views.dis_collect', name='dis_collect'),
    url(r'^user/collection/$', 'reader.views.view_collection', name='view_collection'),

    url(r'^user/mark/(?P<id>(\d+))/$', 'reader.views.mark', name='mark'),
    url(r'^user/dismark/(?P<id>(\d+))/$', 'reader.views.dis_mark', name='dis_mark'),
    url(r'^user/bookmark/$', 'reader.views.view_bookmark', name='view_bookmark'),

    url(r'^user/addnote/(?P<id>(\d+))/$', 'reader.views.take_note', name='take_note'),
    url(r'^user/delnote/(?P<id>(\d+))/$', 'reader.views.delete_note', name='delete_note'),
    url(r'user/note/$', 'reader.views.view_note', name='view_note'),
    
    url(r'^user/account/$', 'reader.views.account', name='account'),
    url(r'^about/$', 'reader.views.about'),
    url(r'^contact/$', 'reader.views.contact'),
)



