from django.contrib import admin
from .models import Profile, Pet, Veterinarian, Store, Pet_Lover, FriendRequest
# Register your models here.

# Register your models here.
admin.site.register(Profile)

admin.site.register(Pet)
admin.site.register(Veterinarian)
admin.site.register(Store)
admin.site.register(Pet_Lover)

admin.site.register(FriendRequest)