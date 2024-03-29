from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User,related_name='Profile', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    email= email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default='photos/avt_default.png',upload_to = "photos/%Y/%m/%d")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)