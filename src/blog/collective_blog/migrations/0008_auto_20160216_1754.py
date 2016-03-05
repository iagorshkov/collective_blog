# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collective_blog', '0007_post_published_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='blog',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]