from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from TopStore.accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if created:
        profile = Profile(
            user=instance,
        )

        profile.save()


@receiver(pre_save, sender=Profile)
def check_for_completed_profile(sender, instance, **kwargs):
    if instance.profile_image:
        instance.is_profile_completed = True
