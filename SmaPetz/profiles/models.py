from ast import Lambda
from itertools import chain
from django.db import models
from matplotlib.style import available
from users.models import User
from phonenumber_field.modelfields import PhoneNumberField
import random

# abstract profile model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    background = models.ImageField(upload_to='backgrounds', default='background.png')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    bio = models.TextField(default="no bio...", blank=True, max_length=255)
    address = models.TextField(max_length=255, blank=True)
    number = PhoneNumberField(unique = True, null = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    #abstract class will not have its own table, instead child classes will have their own tables

class Pet(Profile):
    
    class petTypes(models.TextChoices):
        FISH = "FISH", "Fish"
        REPTILE = "REPTILE", "Reptile"
        BIRD = "BIRD", "Bird"
        AMPHIBIAN = "AMPHIBIAN" ,'Amphibian'
        MAMMAL = "MAMMAL" ,'Mammal'
        OTHER = "OTHER" , 'Other'

    class fishTypes(models.TextChoices):
        BETTA = "BETTA", "Betta"
        GOLDFISH = "GOLDFISH", "Goldfish"
        ANGELFISH = "ANGELFISH", "Angelfish"
        GUPPIES = "GUPPIES" ,'Guppies'
        NEONTETRAS = "NEONTETRAS" ,'Neon Tetras'
        ZEBRADANIOS = "ZEBRADANIOS" ,'Zebra Danios'
        MOLLIES = "MOLLIES" ,'Mollies'
        CATFISH = "CATFISH" ,'Catfish'
        CHERRYBARB = "CHERRYBARB" ,'Cherry Barb'
        PLATY = "PLATY" ,' Platy'
        SWORDTAIL = "SWORDTAIL" ,' Swordtail'
        OTHER = "OTHER" , 'Other'

    class reptileTypes(models.TextChoices):
        BEARDEDDRAGON = "BEARDEDDRAGON", "Bearded Dragon"
        GECKOS = "GECKOS", "Leopard Gecko"
        TURTLES = "TURTLES", "Turtle"
        TORTOISE = "TORTOISE" ,'Tortoise'
        CORNSNAKES = "CORNSNAKES" ,'Corn Snake'
        ZEBRADANIOS = "ZEBRADANIOS" ,'Ball Python'
        CRESTEDGECKO = "CRESTEDGECKO" ,'Crested Gecko'
        SKINK = "SKINK" ,'Blue-Tongued Skink'
        GREENIGUANA = "GREENIGUANA" ,'Green Iguana'
        ANOLE = "ANOLE" ,' Anole'
        SNAKE = "SNAKE" ,'Snake'
        WATERDRAGON = "WATERDRAGON" ,'Water Dragon'
        OTHER = "OTHER" , 'Other'

    class birdTypes(models.TextChoices):
        PARROT = "PARROT", "Parrot"
        COCKTIEL = "COCKTIEL", "Cockatiel"
        FINCH = "FINCH", "Finch"
        COCKATOO = "COCKATOO" ,'Cockatoo'
        CANARY = "CANARY" ,'Canary'
        LOVEBIRD = "LOVEBIRD" ,'Lovebird'
        PARAKEET = "PARAKEET" ,'Parakeet'
        DOVE = "DOVE" ,'Dove'
        CONURES = "CONURES" ,'Conures'
        MACAW = "MACAW" ,'Macaw'
        OTHER = "OTHER" , 'Other'

    class amphibianTypes(models.TextChoices):
        TREEFROG = "TREEFROG", "Tree Frog"
        SALMANDER = "SALMANDER", "Salamander"
        FINCH = "AXOLOTL", "Axolotl"
        PACEMANFROG = "PACEMANFROG" ,'Pacman Frog'
        OFBT = "OFBT" ,'Oriental Fire-Bellied Toad'
        EASTERNNEWT = "EASTERNNEWT" ,'Eastern Newt'
        OTHER = "OTHER" , 'Other'

    class mammalTypes(models.TextChoices):
        GERBIL = "GERBIL", "Gerbil"
        DOG = "DOG", "Dog"
        CAT = "CAT", "Cat"
        HAMSTER = "HAMSTER" ,'Hamster'
        RABBIT = "RABBIT" ,'Rabbit'
        RAT = "RAT" ,'Rat'
        PIG = "PIG" ,'Guinea Pig'
        FERRET = "FERRET" ,'Ferret'
        HEDGEHOG = "HEDGEHOG" ,'Hedgehog'
        FFOXES = "FFOXES" ,' Fennec Foxes'
        OTHER = "OTHER" , 'Other'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pet')
    following = models.ManyToManyField(User, related_name='pet_following', blank=True)
    avatar = models.ImageField(upload_to='avatars', default='pet_avatar.png')
    usertype = models.TextField(default="Pet", blank = True)
    pet_type = models.CharField(max_length=50, choices=petTypes.choices, blank=True)

    fish_type = models.CharField(max_length=50, choices=fishTypes.choices, blank=True)
    reptile_type = models.CharField(max_length=50, choices=reptileTypes.choices, blank=True)
    bird_type = models.CharField(max_length=50, choices=birdTypes.choices, blank=True)
    amphibian_type = models.CharField(max_length=50, choices=amphibianTypes.choices, blank=True)
    mammal_type = models.CharField(max_length=50, choices=mammalTypes.choices, blank=True)
    
    breed = models.TextField(max_length=50, blank=True)

    def __str__(self):
        return str(self.user)


class Veterinarian(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vet') 
    usertype = models.TextField(default="Veterinarian", blank = True)
    following = models.ManyToManyField(User, related_name='vet_following', blank=True)
    education = models.TextField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars', default='vet_avatar.png')

    def __str__(self):
        return str(self.user)
    

class Store(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    class storeTypes(models.TextChoices):
        PETSTORE = "PETSTORE", "Pet Store"
        PRODUCTSTORE = "PRODUCTSTORE", "Pet Product Store"

    avatar = models.ImageField(upload_to='avatars', default='store_avatar.png')
    usertype = models.TextField(default="Store", blank=True)  
    following = models.ManyToManyField(User, related_name='store_following', blank=True)
    store_type = models.CharField(max_length=50, choices=storeTypes.choices, blank=False)
    
    def __str__(self):
        return str(self.user)


class Pet_Lover(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='petLover')
    following = models.ManyToManyField(User, related_name='petLover_following', blank=True)
    usertype = models.TextField(default="Pet Lover", blank=True)  
    avatar = models.ImageField(upload_to='avatars', default='avatar.png')

    def __str__(self):
        return str(self.user)