from django.shortcuts import render, get_object_or_404
from .models import Blog, Post, Comment
from math import ceil

page_post_limit = 5.0

def update_Blogs_and_Posts_by_rating():
    Blogs = Blog.objects.order_by('-rating')[:5]
    Posts = Post.objects.order_by('-rating')[:5]
    return Blogs, Posts

def register(request):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    return render(request, 'collective_blog/register.html', {"Blogs":Top_blogs, "Posts":Top_posts})


def post_detail(request, post_id, blog_id):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    post = get_object_or_404(Post, pk=post_id)
    Comments = Comment.objects.filter(post__pk = post_id)
    return render(request, 'collective_blog/post_detail.html', {"Post":post, "Blogs":Top_blogs, "Posts":Top_posts, "Comments":Comments})

def blog_detail(request, blog_id, page_number=1):
    Top_blogs, Top_posts = update_Blogs_and_Posts_by_rating()
    Current_Blog = Blog.objects.get(name=blog_id)
    count_pages = int(ceil(len(Post.objects.filter(blog__name=blog_id))/page_post_limit))
    Blog_Posts = Post.objects.filter(blog__name=blog_id)[page_post_limit * (int(page_number) - 1):page_post_limit * int(page_number)]
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
