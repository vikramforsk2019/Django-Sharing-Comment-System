from first_app.fun_upload import handle_uploaded_file  #file upload
from .models import User   #Table creation
from .models import Signup,Post,Comment,Genre
from django.shortcuts import render  
#importing loading from django template  
from django.template import loader  
# Create your views here.  
from django.http import HttpResponse  
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import logout
from first_app.templatetags import extras
from django.db import connection
import datetime
from django.utils import timezone
# <----> how to use sql query in django directly?
# <----> take parents id

"""
parents=Comment.objects.raw('''select id,parent_id from first_app_comment where exists ( select 1 from first_app_comment M where M.parent_id = first_app_comment.id)''')
child=Comment.objects.filter(object_id=1)
print(child)
for comment in parents:
	print(comment.id)
	for ch in child:
		if(comment.id==ch.parent_id):
			print('---->',ch.id)
	

cursor = connection.cursor()
cursor.execute('''select id,parent_id from first_app_comment where exists ( select 1 from first_app_comment M where M.parent_id = first_app_comment.id)''')
row = cursor.fetchall()
for e in row:
	print(e[0])
	"""
@csrf_exempt
def signup(request):  
   template = loader.get_template('signup.html') 
   return HttpResponse(template.render())        
@csrf_exempt
def login(request):  
   template = loader.get_template('login.html') 
   return HttpResponse(template.render()) 

@csrf_exempt
def home(request):
	form_data=request.POST
	if request.method == 'POST':
		if request.POST.get('uname') and request.POST.get('email'):
			post=User()
			post.uname= request.POST.get('uname')
			post.email= request.POST.get('email')
			post.file=request.FILES['myfile'].name
			post.save()	
			request.session['semail'] =request.POST.get('email')
			handle_uploaded_file(request.FILES['myfile'])			
			p=User.objects.get(email=request.POST.get('email'))	  
			return render(request, 'profile.html', {'row':p})
@csrf_exempt
def check(request):
	if request.method == 'POST':
		if request.POST.get('uname') and request.POST.get('email'):
			request.session['semail'] =request.POST.get('email')
			p=User.objects.get(email=request.POST.get('email'))	
			return render(request, 'profile.html',{'row': p})

@csrf_exempt
def profile(request): 
	p=User.objects.get(email=request.session.get('semail'))		
	return render(request, 'profile.html',{'row': p})

def logout_view(request):
    logout(request)
    return render(request, 'login.html')

def profile(request): 
	p=User.objects.get(email=request.session.get('semail'))		
	return render(request, 'profile.html',{'row': p})

def createpost(request): 
	return render(request, 'createpost.html')
@csrf_exempt
def createpost_save(request):
    if request.method == 'POST':    	
    	p=User.objects.get(email=request.session.get('semail'))
    	post=Post()
    	post.title= request.POST.get('title')
    	post.body= request.POST.get('body')
    	post.author=p
    	post.save()
    	return render(request, 'profile.html',{'row': p})
    else:
    	return render(request, 'createpost.html')

def postlist(request): 
	p=User.objects.get(email=request.session.get('semail'))
	post=Post.objects.filter(author=p.id)
	#print(post.author.email)  # can access by many(post table) to one (profile table)
	return render(request, 'postlist.html',{'post_data':post})

def postlist_all(request): 
	post=Post.objects.all()
	return render(request, 'postlist.html',{'post_data':post})	
def post_des(request,username):
	p=Post.objects.get(id=username) # post id in username
	c=Comment.objects.filter(object_id=p.id)
	comments=Comment.objects.filter(object_id=p.id,parent_id=None)
	#print(datetime.datetime.now()-c[0].posted)
	return render(request, 'show_comment.html',{'com':c,'raw':p,'genres':Comment.objects.all()})


from django.views.generic import ListView
from .models import Post

class PostList(ListView):
    model = Post
    template_name = 'post/postlist.html'

def show_tree(request):
    return render(request, "show_comment.html", {'genres': Comment.objects.all()})

@csrf_exempt
def comment_post(request): 	
	if request.method == 'POST':
		print('yes request here')
		p=User.objects.get(email=request.session.get('semail'))
		parent_obj = None
		try:
			parent_id = int(request.POST.get('parentid'))
		except: 
			parent_id = None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()
		Comment.objects.create(content=request.POST.get('commentbox'), parent=parent_obj,user=p,object_id=request.POST.get('postid'))
		#post.save()  
		return render(request, "genres.html", {'genres': Comment.objects.all()})   