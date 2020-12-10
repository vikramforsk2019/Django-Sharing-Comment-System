from first_app.fun_upload import handle_uploaded_file  #file upload
from .models import User   #Table creation
from .models import Signup,Post,Comment
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
import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponseRedirect

from first_app.models import Vote
from django.db.models import F
from django.db.models import Q
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
        post.file=request.FILES['myfile'].name
        post.title= request.POST.get('title')
        post.body= request.POST.get('body') 
        post.author=p
        post.save()
        handle_uploaded_file(request.FILES['myfile'])
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
	comments=Comment.objects.filter(object_id=p.id) #only show particular post comment
	main=User.objects.get(email=request.session.get('semail'))
	return render(request, 'show_comment.html',{'com':c,'post':p,'genres':comments,'main':main})

from django.views.generic import ListView
from .models import Post

class PostList(ListView):
    model = Post
    template_name = 'post/postlist.html'

def show_tree(request):
    return render(request, "genres.html", {'genres': Comment.objects.all()})		 
    
@csrf_exempt
def comment_post(request): 	
	if request.method == 'POST':
		print('yes request here')
		rp = json.loads(request.body.decode('utf-8'))
		#print(rp)
		p=User.objects.get(email=request.session.get('semail'))
		parent_obj = None
		try:
			parent_id = int(rp['parentid'])
		except: 
			parent_id = None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()
		Comment.objects.create(content=rp['content'], parent=parent_obj,user=p,object_id=rp['postid'])
		#post.save()
		context = serializers.serialize('json', Comment.objects.all())
		#print(context)
		return JsonResponse({'status': 'Success', 'message': 'Recoard has been updated.'})

def remove_comment(request,commentid):
    comment = Comment.objects.get(id=commentid)
    comment.delete()
    return redirect('post_des',username=comment.object_id)
   # return render(request, "genres.html", {'genres': Comment.objects.all()})
@csrf_exempt
def edit(request):
    rp = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        commentid = int(rp['parentid'])
        ob = Comment.objects.get(id=commentid)
        ob.content=rp['content']
        ob.save()
    return JsonResponse({'status': 'Success', 'message': 'Recoard has been updated.'})


@csrf_exempt
def get(request):
    context= serializers.serialize('json', Comment.objects.all())

@csrf_exempt
def thumbs(request):

    if request.POST.get('action') == 'thumbs':

        id = int(request.POST.get('postid'))
        button = request.POST.get('button')
        update = Comment.objects.get(id=id)
        p=User.objects.get(email=request.session.get('semail'))

        if update.thumbs.filter(id=p.id).exists():

            # Get the users current vote (True/False)
            q = Vote.objects.get(
                Q(comment_id=id) & Q(user_id=p.id))
            evote = q.vote

            if evote == True:

                # Now we need action based upon what button pressed

                if button == 'thumbsup':

                    update.thumbsup = F('thumbsup') - 1
                    update.thumbs.remove(p)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

                if button == 'thumbsdown':

                    # Change vote in Post
                    update.thumbsup = F('thumbsup') - 1
                    update.thumbsdown = F('thumbsdown') + 1
                    update.save()

                    # Update Vote

                    q.vote = False
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

            pass

            if evote == False:

                if button == 'thumbsup':

                    # Change vote in Post
                    update.thumbsup = F('thumbsup') + 1
                    update.thumbsdown = F('thumbsdown') - 1
                    update.save()

                    # Update Vote

                    q.vote = True
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

                if button == 'thumbsdown':

                    update.thumbsdown = F('thumbsdown') - 1
                    update.thumbs.remove(p)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

        else:        # New selection

            if button == 'thumbsup':
                update.thumbsup = F('thumbsup') + 1
                update.thumbs.add(p)
                update.save()
                # Add new vote
                new = Vote(comment_id=id, user_id=p.id, vote=True)
                new.save()
            else:
                # Add vote down
                update.thumbsdown = F('thumbsdown') + 1
                update.thumbs.add(p)
                update.save()
                # Add new vote
                new = Vote(comment_id=id, user_id=p.id, vote=False)
                new.save()

            # Return updated votes
            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown

            return JsonResponse({'up': up, 'down': down})

    pass

