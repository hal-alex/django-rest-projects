from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

# Create your models here.


class UserProfileManager(BaseUserManager):
    """Custom manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user account"""
        if not email: 
            raise ValueError("User must have a valid email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password): 
        """Create a new superuser account"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin): 
    """DB model for registered users"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self): 
        """Fetch full name of the user"""
        return self.name
    
    def get_short_name(self): 
        """Fetch the short name of the user"""
        return self.name

    def __str__(self): 
        """Returns a string version of the user"""
        return self.email
    

class ProfileFeedItem(models.Model): 
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        """Return the model as string"""
        return self.status_text