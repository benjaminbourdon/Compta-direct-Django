from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProfileAC


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_profile_ac")
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileAC.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="maj_profile_ac")
def save_profile(sender, instance, **kwargs):
    instance.profile_ac.save()
