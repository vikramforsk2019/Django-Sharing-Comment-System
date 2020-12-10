from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import os
from django.utils import timezone
# Create your models here.
class User(models.Model):
    uname= models.CharField(max_length=30, unique=True)
    email= models.EmailField()
    file=  models.FileField(default="", editable=False) # for creating file input 

class Signup(models.Model):
	fname=models.CharField(max_length=30)
	lname=models.CharField(max_length=30)
	gender=models.CharField(max_length=30)
	email=models.CharField(max_length=30,unique=True)
	password=models.CharField(max_length=30)
	image=models.FileField()
	class Meta:
		db_table="signup"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=150)
    body = models.TextField()
    file=  models.FileField(default="", editable=False)
    date = models.DateTimeField(default=timezone.now, editable=False)
    editdate = models.DateTimeField(default=timezone.now, editable=False)

class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    object_id = models.PositiveIntegerField(default=0)
    content = models.TextField()
    posted = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(default=timezone.now, editable=False)
    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')
    thumbs = models.ManyToManyField(User, related_name='thumbs', default=None, blank=True)
    class Meta:
        ordering = ['-posted', ]    

class Vote(models.Model):

    comment = models.ForeignKey(Comment, related_name='commentid',
                             on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(User, related_name='userid',
                             on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)


