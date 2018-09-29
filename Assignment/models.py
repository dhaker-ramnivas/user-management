from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

def validate_length(value,length=6):
    if len(str(value))!=length:
        raise ValidationError(u'%s is not the correct length' % value)
# Create your models here.

class TextEntry(models.Model):
    data=models.CharField(max_length=255,validators=[validate_length])
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='textdata')

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE) #1 to 1 link with Django User
    key_expires = models.DateTimeField()


    def __str__(self):
        return self.user.get_username()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1),
                                                     "%Y-%m-%d %H:%M:%S")
            Profile.objects.create(user=instance,key_expires=key_expires)


    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):

        instance.profile.save()
