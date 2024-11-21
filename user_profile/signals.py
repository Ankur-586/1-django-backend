from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import logging
from django.db import transaction

from .models import UserProfile

User = get_user_model()

logger = logging.getLogger('user_profiles')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    logger.debug('Signal received for user: %s, created: %s', instance.username, created)
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f'Creating UserProfile for user: {instance.username}')
    else:
        logger.debug(f'UserProfile not created for user: {instance.username}, user already exists.')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    logger.debug('Signal received for user: %s', instance.username)
    try:
        profile = UserProfile.objects.get(user=instance)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
        logger.info(f'Creating UserProfile for user: {instance.username}')
    else:
        profile.save()
        logger.info(f'Updating UserProfile for user: {instance.username}')
        
