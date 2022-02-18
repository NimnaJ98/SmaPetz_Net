from django.db import models
from users.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Default profile model

class Profile(models.Model):
    PET = 1
    VET = 2
    STORE = 3
    PET_LOVER = 4
    ROLE_CHOICES = (
        (PET, 'Pet'),
        (VET, 'Vet'),
        (STORE, 'Veterinarian'),
        (PET_LOVER, 'Pet Lover'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    type = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=False, blank=False)
    background = models.ImageField(upload_to='backgrounds', default='background.png')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    bio = models.TextField(default="no bio...", blank=True)
    address = models.TextField(max_length=255, blank=True)
    number = PhoneNumberField(unique = True, null = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Pet(Profile):
    
    class petTypes(models.TextChoices):
        CAT = "CAT", "Cat"
        DOG = "DOG", "Dog"
        FISH = "FISH", "Fish"
        HAMSTER = "HAMSTER", "Hamster"
        RABBIT = "RABBIT", "Rabbit"
        MOUSE = "MOUSE", "Mouse"
        TURTLE = "TURTLE", "Turtle"
        REPTILE = "REPTILE", "Reptile"
        BIRD = "BIRD", "Bird"
        AMPHIBIAN = "AMPHIBIAN" ,'Amphibian'
        MAMMAL = "MAMMAL" ,'Mammal'
        OTHER = "OTHER" , 'Other'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pet')
    following = models.ManyToManyField(User, related_name='pet_following', blank=True)
    type = models.PositiveSmallIntegerField(default="PET")
    avatar = models.ImageField(upload_to='avatars', default='pet_avatar.png')
    pet_type = models.CharField(max_length=50, choices=petTypes.choices)
    breed = models.TextField(max_length=50, blank=True)

    def __str__(self):
        return str(self.user)

class Veterinarian(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vet') 
    following = models.ManyToManyField(User, related_name='vet_following', blank=True)
    type = models.PositiveSmallIntegerField(default="VET")
    avatar = models.ImageField(upload_to='avatars', default='vet_avatar.png')

    def __str__(self):
        return str(self.user)

class Store(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    type = models.PositiveSmallIntegerField(default="STORE")
    class storeTypes(models.TextChoices):
        PETSTORE = "PETSTORE", "Pet Store"
        PRODUCTSTORE = "PRODUCTSTORE", "Pet Product Store"

    avatar = models.ImageField(upload_to='avatars', default='store_avatar.png')
    following = models.ManyToManyField(User, related_name='store_following', blank=True)
    store_type = models.CharField(max_length=50, choices=storeTypes.choices, blank=False)
    
    def __str__(self):
        return str(self.user)

class Pet_Lover(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='petLover')
    following = models.ManyToManyField(User, related_name='petLover_following', blank=True)
    type = models.PositiveSmallIntegerField(default="PETLOVER")
    avatar = models.ImageField(upload_to='avatars', default='avatar.png')

    def __str__(self):
        return str(self.user)