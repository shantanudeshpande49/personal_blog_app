from django.urls import path
from . import views

urlpatterns = [
    # path('', views.startingPage, name='starting-page'),
    path('', views.StartingPage.as_view(), name='starting-page'),

    # path('posts/', views.posts, name='posts-page'),
    path('posts/', views.AllPostView.as_view(), name='posts-page'),    

    # path('posts/<slug:slug>', views.postDetail, name='post-detail-page') # posts/my-first-post, my-first-post is called a slug
    path('posts/<slug:slug>', views.SinglePostView.as_view(), name='post-detail-page'),

    path('read-later/', views.ReadLaterView.as_view(), name='read-later')
]
