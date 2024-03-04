from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, photo, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, photo=photo, phone=phone, **extra_fields)
        user.set_password(password)
        if photo:
            user.photo = photo
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, photo=None, phone=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # if self.filter(email,is_superuser=True).exists():
        #     print("A superuser with the email already exists.")
        #     return
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, photo=photo, phone=phone, password=password, **extra_fields)
    

class customUser(AbstractUser):
    email = models.EmailField(max_length=200,unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    # Add any additional fields you need for your user model

    # def save(self, *args, **kwargs):
    #     # If the photo field is empty, set the default URL
    #     if not self.photo:
    #         self.photo.name = 'default_profile_photo.png'  # Set a default file name if needed
    #         self.photo.url = 'https://img.icons8.com/pulsar-line/48/user.png'

    #     super().save(*args, **kwargs)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    

# Provide unique related names for groups and user_permissions
# customUser._meta.get_field('groups').related_query_name = 'custom_user_groups'
# customUser._meta.get_field('user_permissions').related_query_name = 'custom_user_permissions'