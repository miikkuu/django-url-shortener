from django.contrib import admin
from .models import Url, ShortenedURLHistory

# Register your models here.
admin.site.register(Url)
admin.site.register(ShortenedURLHistory)
