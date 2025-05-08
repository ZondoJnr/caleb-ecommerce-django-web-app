from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Store, Product
from utils.twitter import post_tweet 

'''
@receiver(post_save, sender=Store)
def tweet_new_store(sender, instance, created, **kwargs):
    if created:
        tweet = f"🛍️ New Store Added: {instance.name}\n{instance.description}"
        if instance.images:
            post_tweet(tweet, image_path=instance.image.path)
        else:
            post_tweet(tweet)

@receiver(post_save, sender=Product)
def tweet_new_product(sender, instance, created, **kwargs):
    if created:
        tweet = f"🆕 New Product in {instance.store.name}!\n{instance.name}: {instance.description}"
        if instance.image:
            post_tweet(tweet, image_path=instance.image.path)
        else:
            post_tweet(tweet)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
'''