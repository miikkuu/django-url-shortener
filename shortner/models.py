from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Url(models.Model):
    link = models.CharField(max_length=10000)
    uuid = models.CharField(max_length=10)

class ShortenedURLHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shortened_url = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
