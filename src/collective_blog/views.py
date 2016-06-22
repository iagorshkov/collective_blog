#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from .models import Blog, Post, Comment, PostLike
from math import ceil
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import RegistrationForm, LoginForm, AddCommentForm, AddPostForm
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from django_wysiwyg import clean_html
import json
from django.forms.models import fields_for_model, model_to_dict

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

    return render(request, 'collective_blog/register.html', {"Blogs":Top_blogs, "Posts":Top_posts, "RegistrationForm":form, "title":'Registration'})

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

    return render(request, 'collective_blog/login.html', {"Blogs":Top_blogs, "Posts":Top_posts, "LoginForm":form, "title":'Login'})


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
            blog = get_object_or_404(Blog, pk=post.blog.id)
            blog.rating += 1
            blog.save()
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
            blog = get_object_or_404(Blog, pk=post.blog.id)
            blog.rating -= 1
            blog.save()
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
    if not request.user.is_authenticated():
        return custom_handler404(request)
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    blog = Blog.objects.filter(name=blog_id)
    form = AddPostForm(request.POST)
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            new_post = Post(blog = get_object_or_404(Blog, name=blog_id), title = form.cleaned_data['title'], text = form.cleaned_data['text'], published_date=timezone.now(), author=request.user)
            new_post.save()
            return blog_detail(request, blog_id)
    else:
        form = AddPostForm()

    return render(request, 'collective_blog/add_post.html', {"Blogs":Top_blogs, "Posts":Top_posts, "Blog_name":blog[0], "Form":AddPostForm, "title":'Add Post'})

def remove_post(request, blog_id, post_id):
    if not request.user.is_superuser:
        return custom_handler404(request)
    page_number = 1
    post = get_object_or_404(Post, pk=post_id).delete()
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    Current_Blog = Blog.objects.get(name=blog_id)
    count_pages = int(ceil(len(Post.objects.filter(blog__name=blog_id))/page_post_limit))
    Blog_Posts = Post.objects.filter(blog__name=blog_id).order_by('-published_date')[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]

    return render(request, 'collective_blog/blog_detail.html', {"Blog":Current_Blog, "Blog_Posts":Blog_Posts, "Blogs":Top_blogs, "Posts":Top_posts, "count_pages":range(1,count_pages+1), "title":'Blog "' + Current_Blog.full_name + '" by date'})

def remove_comment(request, comment_id, post_id, blog_id):
    if not request.user.is_superuser:
        return custom_handler404(request)
    comment = get_object_or_404(Comment, pk=comment_id).delete()
    form = AddCommentForm()
    post = get_object_or_404(Post, pk=post_id)
    page_number = 1

    Comments = Comment.objects.filter(post__pk = post_id).order_by('-published_date')
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    return render(request, 'collective_blog/post_detail.html', {"Post":post, "Blogs":Top_blogs, "Posts":Top_posts, "Comments":Comments, "AddCommentForm":form, "title":post.title})


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
            form = AddCommentForm()
            return render(request, 'collective_blog/post_detail.html', {"Post":post, "Blogs":Top_blogs, "Posts":Top_posts, "Comments":Comments, "AddCommentForm":form, "title":post.title})

    else:
        form = AddCommentForm()

    return render(request, 'collective_blog/post_detail.html', {"Post":post, "Blogs":Top_blogs, "Posts":Top_posts, "Comments":Comments, "AddCommentForm":form, "title":post.title})

def blog_detail(request, blog_id, page_number=1):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    Current_Blog = Blog.objects.get(name=blog_id)
    count_pages = int(ceil(len(Post.objects.filter(blog__name=blog_id))/page_post_limit))
    Blog_Posts = Post.objects.filter(blog__name=blog_id).order_by('-published_date')[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]
    return render(request, 'collective_blog/blog_detail.html', {"Blog":Current_Blog, "Blog_Posts":Blog_Posts, "Blogs":Top_blogs, "Posts":Top_posts, "count_pages":range(1,count_pages+1), "title":'Blog "' + Current_Blog.full_name + '" by date'})

def by_date_all_page(request, page_number=1):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    count_pages = int(ceil(len(Post.objects.all())/page_post_limit))
    page_posts = Post.objects.order_by('-published_date')[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]
    return render(request, 'collective_blog/by_date_all_page.html', {"Blogs":Top_blogs, "Posts":Top_posts, "Page_posts":page_posts, "count_pages":range(1, count_pages + 1), "title":'Posts by date'})

def by_rating_all_page(request, page_number):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    count_pages = int(ceil(len(Post.objects.all())/page_post_limit))
    page_posts = Post.objects.order_by('-rating')[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]
    return render(request, 'collective_blog/by_rating_all_page.html', {"Blogs":Top_blogs, "Posts":Top_posts, "Page_posts":page_posts, "count_pages":range(1, count_pages + 1), "title":'Posts by rating'})

def blogs_by_rating(request, page_number):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    count_pages = int(ceil(len(Blog.objects.all())/10.0))
    page_blogs = Blog.objects.order_by('-rating')[10 * (int(page_number) - 1):10 * int(page_number)]
    return render(request, 'collective_blog/blogs_by_rating.html', {"Blogs":Top_blogs, "Posts":Top_posts, "count_pages":range(1, count_pages + 1), "Page_Blogs":page_blogs, "title":'Blogs list'})

def by_rating_blog_posts(request, blog_id, page_number=1):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    Current_Blog = Blog.objects.get(name=blog_id)
    count_pages = int(ceil(len(Post.objects.filter(blog__name=blog_id))/page_post_limit))
    Blog_Posts = Post.objects.filter(blog__name=blog_id).order_by('-rating')[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]
    return render(request, 'collective_blog/blog_posts_by_rating.html', {"Blog":Current_Blog, "Blog_Posts":Blog_Posts, "Blogs":Top_blogs, "Posts":Top_posts, "count_pages":range(1,count_pages+1), "title":'Blog "' + Current_Blog.full_name + '" by rating'})

def custom_handler404(request):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    response = render_to_response('collective_blog/404.html', {"Blogs":Top_blogs,"Posts":Top_posts, "title":'Page Not Found'},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response