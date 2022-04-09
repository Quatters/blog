from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField()
    author = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.author}: {self.title}'

class Comment(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        body = self.body
        if len(body) > 64:
            body = body[:64] + '...'
        return f'{self.author}: {body}'
