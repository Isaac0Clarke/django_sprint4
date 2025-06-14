from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/edit/', views.create_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('posts/<int:post_id>/comment/add/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/comment/<int:comment_pk>/edit/', views.add_comment, name='edit_comment'),
    path('posts/<int:post_id>/comment/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
]