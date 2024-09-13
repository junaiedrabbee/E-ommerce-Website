# store/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Customer

@receiver(post_save, sender=User)
def create_or_update_user_related(sender, instance, created, **kwargs):
    if created:
        # Create UserProfile and Customer if they don't exist
        UserProfile.objects.get_or_create(user=instance)
        Customer.objects.get_or_create(user=instance, email=instance.email)
    else:
        # Update UserProfile and Customer if they already exist
        if hasattr(instance, 'profile'):
            instance.profile.save()
        if hasattr(instance, 'customer'):
            instance.customer.save()
