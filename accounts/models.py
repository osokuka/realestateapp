from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from realtors.models import Realtor

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_realtor = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

# Signal to create or update a user's profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

# Signal to create or update a realtor profile based on the user profile
@receiver(post_save, sender=UserProfile)
def create_or_update_realtor_profile(sender, instance, created, **kwargs):
    if instance.is_realtor:
        Realtor.objects.get_or_create(
            user=instance.user,
            defaults={
                'name': instance.user.get_full_name() or instance.user.username,
                'email': instance.user.email,
                'phone': '',  # Default empty, or pull from another field if available
                'description': '',  # Default empty, or customize as needed
            }
        )
    else:
        Realtor.objects.filter(user=instance.user).delete()
        Realtor.objects.filter(user=instance.user).delete()