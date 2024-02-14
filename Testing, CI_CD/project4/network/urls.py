
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createpost", views.create_post, name="createpost"),
    path("<str:owner>", views.user_profile, name="userprofile"),
    path("new/follow", views.follow, name="follow"),
    path("users/following", views.following_page, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:pk>", views.like_post, name="like_post")
]
