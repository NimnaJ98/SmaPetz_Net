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

@receiver(post_save, sender = FriendRequest)
def post_save_follow(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver

    if instance.status == 'accepted':
        if sender_.type == "PET":
            senderProfile = Pet.objects.get(user =sender_)
        elif sender_.type == "VET":
            senderProfile = Veterinarian.objects.get(user =sender_)
        elif sender_.type == "STORE":
            senderProfile = Store.objects.get(user =sender_)
        elif sender_.type == "PET_LOVER":
            senderProfile = Pet_Lover.objects.get(user =sender_)
        senderProfile.following.add(receiver_)
        senderProfile.save()
        if receiver_.type == "PET":
            receiverProfile = Pet.objects.get(user =receiver_)
        elif receiver_.type == "VET":
            receiverProfile = Veterinarian.objects.get(user =receiver_)
        elif receiver_.type == "STORE":
            receiverProfile = Store.objects.get(user =receiver_)
        elif receiver_.type == "PET_LOVER":
            receiverProfile = Pet_Lover.objects.get(user =receiver_)
        receiverProfile.following.add(sender_)
        receiverProfile.save()
