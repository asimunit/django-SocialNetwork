from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .constant import *

# Create your models here.
''


class Post(models.Model):
    description = models.CharField(max_length=1000, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    user_name = models.ForeignKey(User, related_name="user_names", on_delete=models.CASCADE)
    locations = models.CharField(max_length=255, blank=True)
    names = models.CharField(max_length=255, blank=True)
    organisations = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description


class SimilarPost(models.Model):
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='posts', on_delete=models.CASCADE)
    duplicate = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
