from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from PIL import Image
from shops.models import Shop
# class User(auth.models.User, auth.models.PermissionsMixin):
#     def __str__(self):
#         return "@{}".format(self.username)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return "@{}".format(self.user.username)
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class ShopOwner(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    shops = models.ForeignKey(Shop,on_delete=models.CASCADE)

    def __str__(self):
        return "@{}".format(self.user.username)
