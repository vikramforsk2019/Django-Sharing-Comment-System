from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import os
from django.utils import timezone
# Create your models here.
class User(models.Model):
    uname= models.CharField(max_length=30, unique=True)
    email= models.EmailField()
    file=  models.FileField() # for creating file input 

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
    date = models.DateTimeField(auto_now_add=True)
    editdate = models.DateTimeField(auto_now=True)

class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    object_id = models.PositiveIntegerField(default=0)
    content = models.TextField()
    posted = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted', ]    

class Genre(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(default=0)
    content = models.TextField(blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')       
    