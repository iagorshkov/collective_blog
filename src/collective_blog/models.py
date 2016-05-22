from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Blog(models.Model):
     full_name = models.CharField(max_length=70)
     name = models.CharField(max_length=30)
     rating = models.IntegerField(default=0)

     def __str__(self):
        return self.full_name


class Post(models.Model):
     blog = models.ForeignKey('Blog')
     title = models.CharField(max_length=70)
     text = models.TextField()
     rating = models.IntegerField(default=0)
     published_date = models.DateTimeField(
            blank=True, null=True)

     def __str__(self):
        return self.title

class Comment(models.Model):
     post = models.ForeignKey('Post')
     text = models.TextField()
     author = models.ForeignKey(User)
     rating = models.IntegerField(default = 0)
     reply = models.IntegerField(default = 0)
     published_date = models.DateTimeField(
            blank=True, null=True)

class PostLike(models.Model):
     types = ((1, 'Like'), (-1,'Dislike'))
     post = models.ForeignKey('Post')
     author = models.ForeignKey(User)
     type = models.IntegerField(default=0, choices=types)

     def __str__(self):
         return 'post_id:' + str(self.post_id) + ', username:' + str(self.author) + ', type:' + str(self.type)
