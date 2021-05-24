from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager untuk user profiles"""
    def create_user(self, email, name, password=None):
        """Membuat sebuah profile user"""
        if not email:
            raise ValueError("User must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password):
        """Membuat sebuah super user dengan data yang diterima"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Model database untuk user pada sistem"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Mengambil nama full name untuk user"""
        return self.name
    
    def get_short_name(self):
        """mengambil nama pendek untuk user"""
        return self.name
    
    def ___str__(self):
        """mengembalikan strings dari user"""
        return self.email
    

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=1024)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Akan mengambalikan model sebagai string"""
        return self.status_text

