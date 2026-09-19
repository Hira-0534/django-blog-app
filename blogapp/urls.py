from django.urls import path
from .views import edit_post, home, about, post_detail, post_list, create_post, my_posts, delete_post, register, login_view, logout_view

app_name = 'blogapp'

urlpatterns = [
    path('', home, name='home'),
    path('create-post/', create_post, name='create_post'),
    path('about/', about, name='about'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('author/<str:username>/', post_list, name='post_list'), 
    path('edit-post/<int:pk>/', edit_post, name='edit_post'),
    path('my-posts/', my_posts, name='my_posts'),
    path('delete-post/<int:pk>/', delete_post, name='delete_post'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
        path('logout/', logout_view, name='logout'),  # <-- Yeh line add karni hai

]

