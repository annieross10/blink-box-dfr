from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/', default='../default_profile_qohjd5')
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s Profile"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)