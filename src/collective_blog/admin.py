from django.contrib import admin
from .models import Blog, Post, Comment, PostLike

class PostAdmin(admin.ModelAdmin):
    change_form_template = 'collective_blog/admin/change_form.html'

admin.site.register(Blog)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostLike)