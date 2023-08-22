from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='users_followers')
    followers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='users_following')

class Post(models.Model):
    content = models.CharField(max_length=999)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    userPerson = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    usersLiked = models.ManyToManyField(User, blank=True, symmetrical=False, related_name='post_liked')

    def __str__(self):
        return f"A post made by {self.userPerson.username}"
