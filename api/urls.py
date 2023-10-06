from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name="user-login"),
    path('register/', views.RegisterUser.as_view(), name="user_register"),

    path('create-post/', views.CreateNewPost.as_view(), name="create_post"),
    path('posts/', views.PostList.as_view(), name="posts"),
    path('update-post/<str:pk>/', views.UpdatePost.as_view(), name="update_post"),
    path('delete-post/<str:pk>/', views.DeletePost.as_view(), name="delete_post"),

]

