from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('canvas', views.Canvas.as_view(), name='canvas'),
    path('<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
]
