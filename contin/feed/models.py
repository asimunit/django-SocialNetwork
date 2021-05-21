from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    description = models.CharField(max_length=1000, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user_name = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=255)
#     date = models.DateTimeField(default=timezone.now)
