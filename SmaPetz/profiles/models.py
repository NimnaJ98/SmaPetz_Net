from cProfile import Profile
from django.db import models
from users.models import User
from phonenumber_field.modelfields import PhoneNumberField
from itertools import chain
import random
from django.db.models import Q

# profile manager
class ProfileManager(models.Manager):
    #get posts
    def get_user_posts(request):
        current_user = request.user
        return current_user.post_set.all()
    #get no of posts
    @property
    def num_posts(request):
        current_user = request.user
        return current_user.post_set.all().count()
    
    #get the profiles user is following
    def get_following(self):
        return self.following.all()

    def get_following_list(self):
        follower_list = [p for p in self.get_following()]
        return follower_list
    
    #get the following count
    @property
    def get_following_count(self):
        return self.get_following().count()

    #get followers of the user
    def get_followers(self):
        qs = Profile.objects.all()
        followers_list = []
        for follower in qs:
            if self.user in follower.get_following():
                followers_list.append(follower)
        return followers_list
    
    @property
    def get_followers_count(self):
        return len(self.get_followers())
    
    #to get follow suggestions
    def get_Follow_suggestions(self):
        profile = Profile.objects.all().exclude(user = self.user)
        followers_list = [p for p in self.get_following()]
        availableUser = [p.user for p in profile if p.user not in followers_list]
        random.shuffle(availableUser)
        return availableUser[:5]
    
    #to get the posts of each user & their followers
    def feed_posts(self):
        userPosts = self.get_user_posts()
        following =self.get_following_list()
        suggestions = self.get_Follow_suggestions()
        posts =[]
        qs = None
        for f in following:
            followingPosts =  f.post_set.all()
        posts.append(followingPosts)
        for p in suggestions:
            suggestPosts = p.post_set.all()
            posts.append(suggestPosts)
        posts.append(userPosts)
        if len(posts) > 0:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj:obj.created)
        return qs

# base profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    bio = models.TextField(default="no bio...", blank=True, max_length=100)
    address = models.TextField(max_length=100, blank=True)
    number = PhoneNumberField(unique = True, null = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return str(self.user)

class Pet(Profile, ProfileManager):
    
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
    

    def __str__(self):
        return str(self.user)

class Veterinarian(Profile, ProfileManager):
    vet_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    education = models.TextField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars', default='vet_avatar.png')

    def __str__(self):
        return str(self.user)
    

class Store(Profile, ProfileManager):
    class storeTypes(models.TextChoices):
        PETSTORE = "PETSTORE", "Pet Store"
        PRODUCTSTORE = "PRODUCTSTORE", "Pet Product Store"

    store_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    avatar = models.ImageField(upload_to='avatars', default='store_avatar.png')
    store_type = models.CharField(max_length=50, choices=storeTypes.choices, blank=False)
    
    def __str__(self):
        return str(self.user)


class Pet_Lover(Profile, ProfileManager):
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
    def invitationsReceived(self, receiver):
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
