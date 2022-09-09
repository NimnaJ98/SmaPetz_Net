from cProfile import Profile
from django.db import models
from users.models import User
from phonenumber_field.modelfields import PhoneNumberField
from itertools import chain
import random
from django.shortcuts import reverse
from .utils import get_random_code
from django.template.defaultfilters import default, slugify
from django.db.models import Q

# profile manager
class ProfileManager(models.Manager):

    def get_profiles_to_send_requests(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user = sender)
        qs = FriendRequest.objects.filter(Q(sender=profile)|Q(receiver=profile))
        print(qs)

        accepted= set([])
        for req in qs:
            if req.status == 'accepted':
                accepted.add(req.receiver)
                accepted.add(req.sender)
            
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return(available)

    def get_sent_requests(self, sender):
        profile = Profile.objects.get(user = sender)
        qs = FriendRequest.objects.filter(sender=profile)

        sent= set([])
        for req in qs:
            if req.status == 'send':
                sent.add(req.receiver)
                sent.add(req.sender)   
        return sent


    
    #get all profiles except for the logged in user
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
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return str(self.user)
        
    # def get_absolute_url(self):
    #     return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

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

    def get_all_authors_photos(self):
        return self.posts.all().exclude(picture="")
    
    def get_all_authors_videos(self):
        return self.posts.all().exclude(video="")

    #get followers of the user
    def get_followers(self):
        qs = Profile.objects.all()
        followers_list = []
        for p in qs:
            if self.user in p.get_following():
                followers_list.append(p)
        return followers_list
    
    @property
    def get_followers_count(self):
        return len(self.get_followers())
        
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

    #generate a random slug when there're 2 or more profiles with the same name
    __initial_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_name = self.user.name

    def save(self, *args, **kwargs):
        ex =False
        to_slug = self.slug
        if self.user.name != self.__initial_name or self.slug=="":
            if self.user.name:
                to_slug = slugify(str(self.user.name))
                ex = Profile.objects.filter(slug = to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug+" "+ str(get_random_code()))
                    ex = Profile.objects.filter(slug = to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

class Pet(Profile):
    
    class petTypes(models.TextChoices):
        DOG = "DOG", "Dog"
        CAT = "CAT", "Cat"
        HAMSTER = "HAMSTER" ,'Hamster'
        RABBIT = "RABBIT" ,'Rabbit'
        RAT = "RAT" ,'Rat'
        PIG = "PIG" ,'Guinea Pig'
        FERRET = "FERRET" ,'Ferret'
        GOLDFISH = "GOLDFISH", "Goldfish"
        HEDGEHOG = "HEDGEHOG" ,'Hedgehog'
        FFOXES = "FFOXES" ,' Fennec Foxes'
        GECKOS = "GECKOS", "Leopard Gecko"
        TURTLES = "TURTLES", "Turtle"
        TORTOISE = "TORTOISE" ,'Tortoise'
        SNAKE = "SNAKE" ,'Snake'
        PARROT = "PARROT", "Parrot"
        CANARY = "CANARY" ,'Canary'
        LOVEBIRD = "LOVEBIRD" ,'Lovebird'
        OTHER = "OTHER" , 'Other'

    pet_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    pet_type = models.CharField(max_length=50, choices=petTypes.choices, blank=True)    
    breed = models.TextField(max_length=50, blank=True)
    
    objects = ProfileManager()
    def __str__(self):
        return str(self.user)

class Veterinarian(Profile):
    vet_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    education = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return str(self.user)
    

class Store(Profile):
    class storeTypes(models.TextChoices):
        PETSTORE = "PETSTORE", "Pet Store"
        PRODUCTSTORE = "PRODUCTSTORE", "Pet Product Store"

    store_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    store_type = models.CharField(max_length=50, choices=storeTypes.choices, blank=False)
    
    def __str__(self):
        return str(self.user)

    def get_balance(self):
        items = self.items.filter(store_paid=False, order__stores__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(store_paid=True, order__stores__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)


class Pet_Lover(Profile):
    lover_id = models.OneToOneField(Profile, on_delete=models.CASCADE, parent_link=True, primary_key=True)

    def __str__(self):
        return str(self.user)

#Friend Requests Model
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class FriendRequestManager(models.Manager):
    def received_requests(self, receiver):
        qs = FriendRequest.objects.filter(receiver = receiver, status='send')
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
