# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class FulfillUser(models.Model):
    """
    fulfill users model that have specific user information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    happiness = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    hearts = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    score = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=200)

    
class Task(models.Model):
    """
    task models that defines each task information and is related to only one user
    """
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20)
    category = models.ForeignKey(Category)
    due_date = models.DateTimeField()
    done_progress = models.IntegerField()
    score = models.IntegerField()
    user = models.ForeignKey(FulfillUser)

# t = Task(title='a', description='1', difficulty='1', category='b', due_date='2009-12-12', done_progress=12, score=30, user=f)
