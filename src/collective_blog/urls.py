from django.conf.urls import url, include
from . import views
from django.http import HttpResponse
import django.views.defaults

urlpatterns = [
    url(r'^$', views.by_date_all_page, name='by_date_all_page'),
    url(r'^page/(?P<page_number>[0-9]+)/$', views.by_date_all_page, name='by_date_all_page'),
    url(r'^posts/top/page/(?P<page_number>[0-9]+)/$', views.by_rating_all_page, name='by_rating_all_page'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/post/(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^blogs/page/(?P<page_number>[0-9]+)/$', views.blogs_by_rating, name = 'blogs_by_rating'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/page/(?P<page_number>[0-9]+)/$', views.blog_detail, name='blog_detail'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/$', views.blog_detail, name='blog_detail'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/top/page/(?P<page_number>[0-9]+)$', views.by_rating_blog_posts, name='by_rating_blog_posts'),
    url('register/', views.register, name='register'),
    url('login/', views.login, name='login'),
    url('logout/', views.logout, name='logout'),
    url('new_like/', views.new_like, name='new_like'),
    url('new_dislike/', views.new_dislike, name='new_dislike'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/add_post$', views.add_post, name='add_post'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/post/(?P<post_id>[0-9]+)/remove$', views.remove_post, name='remove_post'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/post/(?P<post_id>[0-9]+)/comment/(?P<comment_id>[0-9]+)/remove$', views.remove_comment, name='remove_comment'),
    url(r'^captcha/', include('captcha.urls')),
    ]


