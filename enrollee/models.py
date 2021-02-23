import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.timezone import now

from phone_field import PhoneField

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creating and save a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """Creates and save a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Enrollee(models.Model):
    """Custom user model for enrollement"""

    CHOICES = (
        ('married', 'Married'),
        ('single', 'Single'),
        ('divorsed', 'Divorsed'),
        ('widow', 'Widow'),
        ('widower', 'Widower'),
    )

    NEXT_OF_KIN = (
        ('father', 'Father'),
        ('son', 'Son'),
        ('wife', 'Wife'),
        ('husband', 'Husband'),
        ('mother', 'Mother'),
        ('sister', 'Sister'),
        ('brother', 'Brother'),
        ('relative', 'Relative'),
        ('friend', 'Friend'),
    )

    EMPLOYMENT = (
        ('employed', 'Employed'),
        ('unemployed', 'UnEmployed'),
    )

    GROUP = (
        ('individual', 'Individual'),
        ('group', 'Group'),
    )

    enrollment_officer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='officer', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    # date_of_birth = models.DateField(blank=False)
    martial_status = models.CharField(max_length=255, choices = CHOICES)
    group_type = models.CharField(max_length=255, choices = GROUP)
    group_size = models.IntegerField(blank=True, default=0)
    next_of_kin_phone_number = models.CharField(max_length=255)
    next_of_kin_name = models.CharField(max_length=255)
    next_of_kin_relationship = models.CharField(max_length=255, choices = NEXT_OF_KIN)
    employment_status = models.CharField(max_length=255, choices = EMPLOYMENT)
    policy_id = models.CharField(max_length=255)
    has_subscribed = models.BooleanField(default=False)
    enrollment_address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=2)
    longitude = models.DecimalField(max_digits=9, decimal_places=2)
    registeration_date = models.DateTimeField(default=now, blank=False)

    def __str__(self):
        return self.enrollment_officer.email
