from django.urls import path, re_path

from .views import (
    createpost_view,goto
)


app_name = 'post'

urlpatterns = [
  path('', createpost_view, name='createpost'),
  path('create/', goto, name='createpost'),
]
