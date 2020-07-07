from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from api.models import LargeCategory, MediumCategory, SmallCategory, Area
from .managers import UserManager
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=45, unique=True)
    nickname = models.CharField(max_length=45)
    business_exp = models.BooleanField(default=False)
    interest_area = models.CharField(max_length=45,blank=True)

    phone = models.CharField(max_length=45)
    is_admin = models.BooleanField(default=False)    
    is_active = models.BooleanField(default=True)    
    is_staff = models.BooleanField(default=False)     

    objects = UserManager()    
    USERNAME_FIELD = 'email'