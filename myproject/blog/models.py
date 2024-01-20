from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length = 120)
    description = models.TextField(blank=True)
    author = models.TextField(blank=True)
    def __str__(self):
        return  self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    