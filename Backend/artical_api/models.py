from django.db import models
from django.contrib.auth.models import User


class Character (models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    characters = models.ManyToManyField(Character,related_name='articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_author')

    def __str__(self):
        return self.title
