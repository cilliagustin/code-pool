from . import views
from django.urls import path


urlpatterns = [
    path('', views.IndexPostList.as_view(), name='home'),
    path('posts', views.AllPostList.as_view(), name='posts'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path(
        'category/delete_comment/<int:pk>',
        views.DeleteComment.as_view(), name='delete_comment'),
    path(
        'approve_comment/<int:pk>/', views.ApproveComment.as_view(),
        name='approve_comment'),
    path(
        'add_remove_bookmark/<slug:slug>',
        views.PostBookmark.as_view(), name='post_bookmark'),
    path(
        "post/<slug:slug>/rate/",
        views.RatingView.as_view(), name="post_rating"),
    path(
        'posts/filter/category/<str:category>',
        views.FilterCategory.as_view(), name='category'),
    path(
        'posts/filter/bookmarked',
        views.FilterBookmark.as_view(), name='bookmark_posts'),
    path(
        'posts/edit_post/<slug:slug>',
        views.EditPost.as_view(), name='edit_post'),
    path(
        'posts/delete_post/<slug:slug>',
        views.DeletePost.as_view(), name='delete_post'),
    path('new_post/', views.CreatePost.as_view(), name='add_post'),
    path('new_category/', views.CreateCategory.as_view(), name='add_category'),
    path('category_list/', views.CategoryList.as_view(), name='category_list'),
    path(
        'category/edit_category/<int:pk>',
        views.EditCategory.as_view(), name='edit_category'),
    path(
        'category/delete_category/<int:pk>',
        views.DeleteCategory.as_view(), name='delete_category'),
    path('canvas', views.Canvas.as_view(), name='canvas'),
]
