from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Profile to hold user images
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        # if the image is larger than 300 pixels
        if img.height > 300 or img.width > 300:
            #resize to 300 pixels
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
