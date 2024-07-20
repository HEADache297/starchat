from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', default='default_profile.jpg')
    slug=models.SlugField(blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.email.split('@')[0])

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username