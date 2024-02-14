from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")

class Post(models.Model):
    content = models.CharField(max_length=5000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    likes = models.ManyToManyField(User, through="Like", related_name="liked_posts")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} publised: {self.content} {self.likes.count()}. {self.timestamp}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # You can add more fields here if you want

    def __str__(self):
        return f"{self.user} liked {self.post}"