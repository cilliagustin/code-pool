from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('canvas', views.Canvas.as_view(), name='canvas'),
    path('new_post/', views.CreatePost.as_view(), name='add_post'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
]
