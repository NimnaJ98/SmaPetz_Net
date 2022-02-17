from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# Create custom model manager

class MyUserManager(BaseUserManager):
    def create_user(self, email, type, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            type=type,
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, type, name, password=None):
        user = self.create_user(
            email,
            password=password,
            type=type,
            name = name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#create custom user model

class User(AbstractBaseUser):
    class Types(models.TextChoices):
        PET = "PET", "Pet"
        VET = "VET", "Veterinarian"
        STORE = "STORE", "Store"
        PET_LOVER = "PET_LOVER", "Pet lover"

    email = models.EmailField(max_length=255,unique=True)
    type = models.CharField(max_length=50, choices=Types.choices, default=Types.PET_LOVER)
    name = models.CharField(blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'type']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"

        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        
        return self.is_admin