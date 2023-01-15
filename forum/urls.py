from . import views
from django.urls import path


urlpatterns = [
    path('', views.IndexPostList.as_view(), name='home'),
    path('posts', views.AllPostList.as_view(), name='posts'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('posts/category/<str:category>', views.FilterCategory.as_view(), name='category'),
    path('posts/edit_post/<slug:slug>', views.EditPost.as_view(), name='edit_post'),
    path('posts/delete_post/<slug:slug>', views.DeletePost.as_view(), name='delete_post'),
    path('new_post/', views.CreatePost.as_view(), name='add_post'),
    path('canvas', views.Canvas.as_view(), name='canvas'),
]
