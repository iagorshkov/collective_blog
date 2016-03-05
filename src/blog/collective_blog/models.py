from __future__ import unicode_literals

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
     rating = models.IntegerField(default = 0)
     reply = models.IntegerField(default = 0)
     published_date = models.DateTimeField(
            blank=True, null=True)

     def __str__(self):
         return self.text
