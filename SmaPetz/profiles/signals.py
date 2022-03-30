from users.models import User
from .models import Profile, Pet, Veterinarian, Store, Pet_Lover, FriendRequest
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender = User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.type == "PET":
            Pet.objects.create(user=instance)       
        elif instance.type == "VET":
            Veterinarian.objects.create(user=instance) 
        elif instance.type == "STORE":
            Store.objects.create(user=instance) 
        elif instance.type == "PET_LOVER":
            Pet_Lover.objects.create(user=instance) 



#whenever a user accepted friends invitation, the user will be included in the friends list.
@receiver(post_save, sender=FriendRequest)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ =instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.following.add(receiver_.user)
        receiver_.following.add(sender_.user)
        sender_.save()
        receiver_.save()