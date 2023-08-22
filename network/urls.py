
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("send", views.send, name="send"),
    path("profile/<str:userPerson>", views.profile, name="profile"),
    path("follow/<str:userFollowing>", views.follow, name="follow"),
    path("unfollow/<str:userUnfollowing>", views.unfollow, name="unfollow"),
    path("following/<str:username>", views.following, name="following"),
    path("next/<int:pageNumber>", views.next, name="next"),
    path("previous/<int:pageNumber>", views.previous, name="previous"), 
    path("update-like/<str:action>/<int:postId>/", views.tempUpdate, name="update-like"),
]
