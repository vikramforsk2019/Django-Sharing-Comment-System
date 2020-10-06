from django.contrib import admin
from django.urls import path, include,re_path
from first_app import views

from first_app.views import PostList
app_name = 'first_app'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup,name='signup'),
    path('home/', views.home),
 path('login/', views.login),
 path('check/', views.check),
 path('profile/', views.profile),
 path('logout/', views.logout_view),
path('createpost/', views.createpost),
path('createpost_save/', views.createpost_save),
path('postlist/', views.postlist),
path('postlist_all/', views.postlist_all),
    re_path(r'^post_des/(?P<username>[.@_+\w-]+)$', views.post_des, name='post_des'),
path('comment_post/', views.comment_post,name='comment_post'),
 path('postlist_view/', PostList.as_view(),name='postlist_view'),
 path('show_tree/', views.show_tree),

 
]
