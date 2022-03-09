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
    usertype1 = models.TextField(default="Pet", blank=True)
    following = models.ManyToManyField(User, related_name='pet_following', blank=True)
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
        qs1 = Pet.objects.all()
        qs2 = Veterinarian.objects.all()
        qs3 = Store.objects.all()
        qs4 = Pet_Lover.objects.all()
        followers_list = []
        for pet in qs1:
            if self.user in pet.get_following():
                followers_list.append(pet)
        for vet in qs2:
            if self.user in vet.get_following():
                followers_list.append(vet)
        for store in qs3:
            if self.user in store.get_following():
                followers_list.append(store)
        for petlover in qs4:
            if self.user in petlover.get_following():
                followers_list.append(petlover)
        return followers_list
    
    @property
    def get_followers_count(self):
        return len(self.get_followers())


    #to get the posts of each user & their followers
    def feed_posts(self):
        userPosts = self.get_user_posts()
        following =self.get_following_list()
        posts =[]
        qs = None
        for f in following:
            followingPosts =  f.post_set.all()
            posts.append(followingPosts)
        posts.append(userPosts)
        if len(posts) > 0:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj:obj.created)
        return qs

    #to get follow suggestions
    def get_Petfollow_suggestions(self):
        pets = Pet.objects.all().exclude(user = self.user)
        followers_list = [p for p in self.get_following()]
        availablePets = [p.user for p in pets if p.user not in followers_list]
        random.shuffle(availablePets)
        return availablePets[:3]

    def get_Vetfollow_suggestions(self):
        vets = Veterinarian.objects.all()
        followers_list = [p for p in self.get_following()]
        availableVets = [p.user for p in vets if p.user not in followers_list]
        random.shuffle(availableVets)
        return availableVets[:3]

    def get_Storefollow_suggestions(self):
        stores = Store.objects.all()        
        followers_list = [p for p in self.get_following()]
        availableStores = [p.user for p in stores if p.user not in followers_list]
        random.shuffle(availableStores)
        return availableStores[:3]

    def get_PetLoverfollow_suggestions(self):
        petLovers = Pet_Lover.objects.all()
        followers_list = [p for p in self.get_following()]
        availablePetLovers = [p.user for p in petLovers if p.user not in followers_list]
        random.shuffle(availablePetLovers)
        return availablePetLovers[:3]



class Veterinarian(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vet') 
    following = models.ManyToManyField(User, related_name='vet_following', blank=True)
    usertype2 = models.TextField(default="Veterinarian", blank=True)    
    avatar = models.ImageField(upload_to='avatars', default='vet_avatar.png')

    def __str__(self):
        return str(self.user)
    
    def get_user_posts(request):
        current_user = request.user
        return current_user.post_set.all()
    
    @property
    def num_posts(request):
        current_user = request.user
        return current_user.post_set.all().count()

    def get_following(self):
        return self.following.all()

    def get_following_list(self):
        follower_list = [p for p in self.get_following()]
        return follower_list
    
    @property
    def get_following_count(self):
        return self.get_following().count()
    
    def get_followers(self):
        qs1 = Pet.objects.all()
        qs2 = Veterinarian.objects.all()
        qs3 = Store.objects.all()
        qs4 = Pet_Lover.objects.all()
        followers_list = []
        for pet in qs1:
            if self.user in pet.get_following():
                followers_list.append(pet)
        for vet in qs2:
            if self.user in vet.get_following():
                followers_list.append(vet)
        for store in qs3:
            if self.user in store.get_following():
                followers_list.append(store)
        for petlover in qs4:
            if self.user in petlover.get_following():
                followers_list.append(petlover)
        return followers_list
    
    @property
    def get_followers_count(self):
        return len(self.get_followers())

    def feed_posts(self):
        userPosts = self.get_user_posts()
        following =self.get_following_list()
        posts =[]
        qs = None
        for f in following:
            followingPosts =  f.post_set.all()
            posts.append(followingPosts)
        posts.append(userPosts)
        if len(posts) > 0:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj:obj.created)
        return qs

    def get_Vetfollow_suggestions(self):
        vets = Veterinarian.objects.all().exclude(user = self.user)
        followers_list = [p for p in self.get_following()]
        availableVets = [p.user for p in vets if p.user not in followers_list]
        random.shuffle(availableVets)
        return availableVets[:3]

    def get_Petfollow_suggestions(self):
        pets = Pet.objects.all()
        followers_list = [p for p in self.get_following()]
        availablePets = [p.user for p in pets if p.user not in followers_list]
        random.shuffle(availablePets)
        return availablePets[:3]
    
    def get_Storefollow_suggestions(self):
        stores = Store.objects.all()        
        followers_list = [p for p in self.get_following()]
        availableStores = [p.user for p in stores if p.user not in followers_list]
        random.shuffle(availableStores)
        return availableStores[:3]

    def get_PetLoverfollow_suggestions(self):
        petLovers = Pet_Lover.objects.all()
        followers_list = [p for p in self.get_following()]
        availablePetLovers = [p.user for p in petLovers if p.user not in followers_list]
        random.shuffle(availablePetLovers)
        return availablePetLovers[:3]
    

class Store(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    usertype3 = models.TextField(default="Store", blank=True)  
    class storeTypes(models.TextChoices):
        PETSTORE = "PETSTORE", "Pet Store"
        PRODUCTSTORE = "PRODUCTSTORE", "Pet Product Store"

    avatar = models.ImageField(upload_to='avatars', default='store_avatar.png')
    following = models.ManyToManyField(User, related_name='store_following', blank=True)
    store_type = models.CharField(max_length=50, choices=storeTypes.choices, blank=False)
    
    def __str__(self):
        return str(self.user)

    def get_user_posts(request):
        current_user = request.user
        return current_user.post_set.all()
    
    @property
    def num_posts(request):
        current_user = request.user
        return current_user.post_set.all().count()
    
    def get_following(self):
        return self.following.all()

    def get_following_list(self):
        follower_list = [p for p in self.get_following()]
        return follower_list
    
    @property
    def get_following_count(self):
        return self.get_following().count()

    #get the count of followers
    @property
    def get_following_count(self):
        return self.get_following().count()

    #get followers based on their user profiles
    def get_followers(self):
        qs1 = Pet.objects.all()
        qs2 = Veterinarian.objects.all()
        qs3 = Store.objects.all()
        qs4 = Pet_Lover.objects.all()
        followers_list = []
        for pet in qs1:
            if self.user in pet.get_following():
                followers_list.append(pet)
        for vet in qs2:
            if self.user in vet.get_following():
                followers_list.append(vet)
        for store in qs3:
            if self.user in store.get_following():
                followers_list.append(store)
        for petlover in qs4:
            if self.user in petlover.get_following():
                followers_list.append(petlover)
        return followers_list
    
    @property
    def get_followers_count(self):
        return len(self.get_followers())
    
    def feed_posts(self):
        userPosts = self.get_user_posts()
        following =self.get_following_list()
        posts =[]
        qs = None
        for f in following:
            followingPosts =  f.post_set.all()
            posts.append(followingPosts)
        posts.append(userPosts)
        if len(posts) > 0:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj:obj.created)
        return qs

    
    def get_Storefollow_suggestions(self):
        stores = Store.objects.all().exclude(user = self.user)        
        followers_list = [p for p in self.get_following()]
        availableStores = [p.user for p in stores if p.user not in followers_list]
        random.shuffle(availableStores)
        return availableStores[:3]

    def get_Vetfollow_suggestions(self):
        vets = Veterinarian.objects.all()
        followers_list = [p for p in self.get_following()]
        availableVets = [p.user for p in vets if p.user not in followers_list]
        random.shuffle(availableVets)
        return availableVets[:3]

    def get_Petfollow_suggestions(self):
        pets = Pet.objects.all()
        followers_list = [p for p in self.get_following()]
        availablePets = [p.user for p in pets if p.user not in followers_list]
        random.shuffle(availablePets)
        return availablePets[:3]

    def get_PetLoverfollow_suggestions(self):
        petLovers = Pet_Lover.objects.all()
        followers_list = [p for p in self.get_following()]
        availablePetLovers = [p.user for p in petLovers if p.user not in followers_list]
        random.shuffle(availablePetLovers)
        return availablePetLovers[:3]

class Pet_Lover(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='petLover')
    following = models.ManyToManyField(User, related_name='petLover_following', blank=True)
    usertype4 = models.TextField(default="Pet Lover", blank=True)  
    avatar = models.ImageField(upload_to='avatars', default='avatar.png')

    def __str__(self):
        return str(self.user)

    def get_user_posts(request):
        current_user = request.user
        return current_user.post_set.all()

    @property
    #property method will be treated as a field
    def num_posts(request):
        current_user = request.user
        return current_user.post_set.all().count()

    def get_following(self):
        return self.following.all()

    def get_following_list(self):
        follower_list = [p for p in self.get_following()]
        return follower_list

    @property
    def get_following_count(self):
        return self.get_following().count()

    #get the count of followers
    @property
    def get_following_count(self):
        return self.get_following().count()

    #get followers based on their user profiles
    def get_followers(self):
        qs1 = Pet.objects.all()
        qs2 = Veterinarian.objects.all()
        qs3 = Store.objects.all()
        qs4 = Pet_Lover.objects.all()
        followers_list = []
        for pet in qs1:
            if self.user in pet.get_following():
                followers_list.append(pet)
        for vet in qs2:
            if self.user in vet.get_following():
                followers_list.append(vet)
        for store in qs3:
            if self.user in store.get_following():
                followers_list.append(store)
        for petlover in qs4:
            if self.user in petlover.get_following():
                followers_list.append(petlover)
        return followers_list
    
    @property
    def get_followers_count(self):
        return len(self.get_followers())

    def feed_posts(self):
        userPosts = self.get_user_posts()
        following =self.get_following_list()
        posts =[]
        qs = None
        for f in following:
            followingPosts =  f.post_set.all()
            posts.append(followingPosts)
        posts.append(userPosts)
        if len(posts) > 0:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj:obj.created)
        return qs

    
    def get_PetLoverfollow_suggestions(self):
        petLovers = Pet_Lover.objects.all().exclude(user = self.user)    
        followers_list = [p for p in self.get_following()]
        availablePetLovers = [p.user for p in petLovers if p.user not in followers_list]
        random.shuffle(availablePetLovers)
        return availablePetLovers[:3]

    def get_Storefollow_suggestions(self):
        stores = Store.objects.all()    
        followers_list = [p for p in self.get_following()]
        availableStores = [p.user for p in stores if p.user not in followers_list]
        random.shuffle(availableStores)
        return availableStores[:3]

    def get_Vetfollow_suggestions(self):
        vets = Veterinarian.objects.all()
        followers_list = [p for p in self.get_following()]
        availableVets = [p.user for p in vets if p.user not in followers_list]
        random.shuffle(availableVets)
        return availableVets[:3]

    def get_Petfollow_suggestions(self):
        pets = Pet.objects.all()
        followers_list = [p for p in self.get_following()]
        availablePets = [p.user for p in pets if p.user not in followers_list]
        random.shuffle(availablePets)
        return availablePets[:3]
