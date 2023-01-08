from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('posts/edit_post/<slug:slug>', views.EditPost.as_view(), name='edit_post'),
    path('new_post/', views.CreatePost.as_view(), name='add_post'),
    path('canvas', views.Canvas.as_view(), name='canvas'),
]
