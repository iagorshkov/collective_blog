#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from .models import Blog, Post, Comment, PostLike
from math import ceil
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import RegistrationForm, LoginForm, AddCommentForm, AddPostForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from django_wysiwyg import clean_html
import json

page_post_limit = 5.0

def update_Blogs_and_Posts_by_rating():
    Blogs = Blog.objects.order_by('-rating')[:5]
    Posts = Post.objects.order_by('-rating')[:5]
    return Blogs, Posts

def register(request):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            check_user = User.objects.filter(username=form.cleaned_data['login']).count()
            if check_user == 0:
                new_user = User.objects.create_user(username = form.cleaned_data['login'], password = form.cleaned_data['password'])
                return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'collective_blog/register.html', {"Blogs":Top_blogs, "Posts":Top_posts, "RegistrationForm":form})

def login(request):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    form = LoginForm(request.POST)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login'],
                                password=form.cleaned_data['password'])
            auth.login(request,user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()

    return render(request, 'collective_blog/login.html', {"Blogs":Top_blogs, "Posts":Top_posts, "LoginForm":form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def new_like(request):
    post = get_object_or_404(Post, pk=request.GET['post_id'])
    response = {}
    response['result'] = ''
    if request.user.is_authenticated():
        check_like = PostLike.objects.filter(author = request.user, post=post, type=1).count()
        if check_like == 0:
            post.rating += 1
            post.save()
            check_dislike = PostLike.objects.filter(author = request.user, post=post, type=-1).count()
            if check_dislike == 1:
                PostLike.objects.get(author = request.user, post=post, type=-1).delete()
            else:
                new_PostLike = PostLike(author = request.user, post=post, type=1)
                new_PostLike.save()
        else:
            response['result'] = 'Вы уже лайкали эту запись'
    else:
        response['result'] = 'Пожалуйста, авторизуйтесь'
    response['rating'] = post.rating

    return HttpResponse(json.dumps(response), content_type="application/json")

def new_dislike(request):
    post = get_object_or_404(Post, pk=request.GET['post_id'])
    response = {}
    response['result'] = ''
    if request.user.is_authenticated():
        check_dislike = PostLike.objects.filter(author = request.user, post=post, type=-1).count()
        if check_dislike == 0:
            post.rating -= 1
            post.save()
            check_like = PostLike.objects.filter(author = request.user, post=post, type=1).count()
            if check_like == 1:
                PostLike.objects.get(author = request.user, post=post, type=1).delete()
            else:
                new_PostLike = PostLike(author = request.user, post=post, type=-1)
                new_PostLike.save()
        else:
            response['result'] = 'Вы уже дислайкали эту запись'
    else:
        response['result'] = 'Пожалуйста, авторизуйтесь'
    response['rating'] = post.rating

    return HttpResponse(json.dumps(response), content_type="application/json")

def add_post(request, blog_id):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    blog = Blog.objects.filter(name=blog_id)
    form = AddPostForm(request.POST)
    if request.method == 'POST':
        print request.POST
        print 'lol'
        if form.is_valid():
            print form.cleaned_data
    else:
        form = AddPostForm()

    return render(request, 'collective_blog/add_post.html', {"Blogs":Top_blogs, "Posts":Top_posts, "Blog_name":blog[0], "Form":AddPostForm})

def post_detail(request, post_id, blog_id):
    form = AddCommentForm()
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    post = get_object_or_404(Post, pk=post_id)
    Comments = Comment.objects.filter(post__pk = post_id).order_by('-published_date')
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment(text=form.cleaned_data['text'], post=get_object_or_404(Post, pk=post_id), published_date=timezone.now(), author=request.user)
            new_comment.save()
            return render(request, 'collective_blog/post_detail.html', {"Post":post, "Blogs":Top_blogs, "Posts":Top_posts, "Comments":Comments, "AddCommentForm":form})

    else:
        form = AddCommentForm()

    return render(request, 'collective_blog/post_detail.html', {"Post":post, "Blogs":Top_blogs, "Posts":Top_posts, "Comments":Comments, "AddCommentForm":form})

def blog_detail(request, blog_id, page_number=1):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    Current_Blog = Blog.objects.get(name=blog_id)
    count_pages = int(ceil(len(Post.objects.filter(blog__name=blog_id))/page_post_limit))
    Blog_Posts = Post.objects.filter(blog__name=blog_id).order_by('-published_date')[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]
    return render(request, 'collective_blog/blog_detail.html', {"Blog":Current_Blog, "Blog_Posts":Blog_Posts, "Blogs":Top_blogs, "Posts":Top_posts, "count_pages":range(1,count_pages+1)})

def by_date_all_page(request, page_number=1):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    count_pages = int(ceil(len(Post.objects.all())/page_post_limit))
    page_posts = Post.objects.order_by('-published_date')[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]
    return render(request, 'collective_blog/by_date_all_page.html', {"Blogs":Top_blogs, "Posts":Top_posts, "Page_posts":page_posts, "count_pages":range(1, count_pages + 1)})

def by_rating_all_page(request, page_number):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    count_pages = int(ceil(len(Post.objects.all())/page_post_limit))
    page_posts = Post.objects.order_by('-rating')[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]
    return render(request, 'collective_blog/by_rating_all_page.html', {"Blogs":Top_blogs, "Posts":Top_posts, "Page_posts":page_posts, "count_pages":range(1, count_pages + 1)})

def blogs_by_rating(request, page_number):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    count_pages = int(ceil(len(Blog.objects.all())/10.0))
    page_blogs = Blog.objects.order_by('-rating')[10 * (int(page_number) - 1):10 * int(page_number)]
    return render(request, 'collective_blog/blogs_by_rating.html', {"Blogs":Top_blogs, "Posts":Top_posts, "count_pages":range(1, count_pages + 1), "Page_Blogs":page_blogs})

def by_rating_blog_posts(request, blog_id, page_number=1):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    Current_Blog = Blog.objects.get(name=blog_id)
    count_pages = int(ceil(len(Post.objects.filter(blog__name=blog_id))/page_post_limit))
    Blog_Posts = Post.objects.filter(blog__name=blog_id).order_by('-rating')[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]
    return render(request, 'collective_blog/blog_posts_by_rating.html', {"Blog":Current_Blog, "Blog_Posts":Blog_Posts, "Blogs":Top_blogs, "Posts":Top_posts, "count_pages":range(1,count_pages+1)})

