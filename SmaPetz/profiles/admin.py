from django.contrib import admin
from .models import Profile, Pet, Veterinarian, Store, Pet_Lover

# Register your models here.


@admin.register(Pet)
class FonteAdmin(admin.ModelAdmin):
     readonly_fields = ['type']

@admin.register(Veterinarian)
class FonteAdmin(admin.ModelAdmin):
     readonly_fields = ['type']

@admin.register(Store)
class FonteAdmin(admin.ModelAdmin):
     readonly_fields = ['type']

@admin.register(Pet_Lover)
class FonteAdmin(admin.ModelAdmin):
     readonly_fields = ['type']

