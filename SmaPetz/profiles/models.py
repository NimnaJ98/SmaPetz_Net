from cProfile import Profile
from django.db import models
from users.models import User
from phonenumber_field.modelfields import PhoneNumberField
from itertools import chain
import random
from django.db.models import Q

# profile manager
class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = FriendRequest.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)
        print("#########")

        accepted= set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)
        print("#########")

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        print("#########")
        return available


    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

# base profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    profilePic = models.ImageField(upload_to='avatars', default='pet_avatar.png')
    bio = models.TextField(default="no bio...", blank=True, max_length=100)
    address = models.TextField(max_length=100, blank=True)
    number = PhoneNumberField(unique = True, null = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return str(self.user)

    #to grab all the following profiles
    def get_following(self):
        return self.following.all()

    #to grab all the count of friends to show in Profile
    def get_following_no(self):
        return self.following.all().count()

    #to grab all the count of posts to show in Profile
    def get_post_no(self):
        return self.posts.all().count()

    #to grab all the posts to show in Profile
    def get_all_authors_posts(self):
        return self.posts.all()

    #to grab the no of likes given by the user
    def get_likes_given_no(self):
        Likes = self.like_set.all()
        total_liked = 0
        for item in Likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    #to grab the no of likes the user was received
    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.like_set.all().count()
        return total_liked

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

    pet_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    avatar = models.ImageField(upload_to='avatars', default='pet_avatar.png')
    pet_type = models.CharField(max_length=50, choices=petTypes.choices, blank=True)

    fish_type = models.CharField(max_length=50, choices=fishTypes.choices, blank=True)
    reptile_type = models.CharField(max_length=50, choices=reptileTypes.choices, blank=True)
    bird_type = models.CharField(max_length=50, choices=birdTypes.choices, blank=True)
    amphibian_type = models.CharField(max_length=50, choices=amphibianTypes.choices, blank=True)
    mammal_type = models.CharField(max_length=50, choices=mammalTypes.choices, blank=True)
    
    breed = models.TextField(max_length=50, blank=True)
    
    objects = ProfileManager()
    def __str__(self):
        return str(self.user)

class Veterinarian(Profile):
    vet_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    education = models.TextField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars', default='vet_avatar.png')

    def __str__(self):
        return str(self.user)
    

class Store(Profile):
    class storeTypes(models.TextChoices):
        PETSTORE = "PETSTORE", "Pet Store"
        PRODUCTSTORE = "PRODUCTSTORE", "Pet Product Store"

    store_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    avatar = models.ImageField(upload_to='avatars', default='store_avatar.png')
    store_type = models.CharField(max_length=50, choices=storeTypes.choices, blank=False)
    
    def __str__(self):
        return str(self.user)


class Pet_Lover(Profile):
    lover_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    avatar = models.ImageField(upload_to='avatars', default='avatar.png')

    def __str__(self):
        return str(self.user)

#Friend Requests Model
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class FriendRequestManager(models.Manager):
    def invitations_received(self, receiver):
        qs = FriendRequest.objects.filter(receiver=receiver, status='send')
        return qs

# FriendRequest model
class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = FriendRequestManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
