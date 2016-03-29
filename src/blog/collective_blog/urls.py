from django.conf.urls import url
from . import views
from django.http import HttpResponse

urlpatterns = [
    url(r'^$', views.by_date_all_page, name='by_date_all_page'),
    url(r'^page/(?P<page_number>[0-9]+)/$', views.by_date_all_page, name='by_date_all_page'),
    url(r'^posts/top/page/(?P<page_number>[0-9]+)/$', views.by_rating_all_page, name='by_rating_all_page'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/post/(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^blogs/page/(?P<page_number>[0-9]+)/$', views.blogs_by_rating, name = 'blogs_by_rating'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/page/(?P<page_number>[0-9]+)/$', views.blog_detail, name='blog_detail'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/$', views.blog_detail, name='blog_detail'),
    url(r'^blog/(?P<blog_id>[a-zA-Z0-9]+)/top/page/(?P<page_number>[0-9]+)$', views.by_rating_blog_posts, name='by_rating_blog_posts'),
    url('register/', views.register, name='register'),]

