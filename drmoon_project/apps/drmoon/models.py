from django.db import models
from django.contrib.auth.models import User
import random

class UserProfile(models.Model):
  user = models.ForeignKey(User,unique=True)

  created  = models.DateTimeField(auto_now_add = True)
  modified = models.DateTimeField(auto_now = True)
  expired  = models.DateTimeField(null = True, blank = True)

  def _generate_request_code():
    nine_digit_number = unicode(random.randint(0,999999999))
    return u'00x' + nine_digit_number.rjust(9,u'0')

  request_code = models.CharField(max_length=12,unique=True,default=_generate_request_code())

## Extra Signal hook
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created: 
        profile, new = UserProfile.objects.get_or_create(user=instance)
## End UserProfile Class


class NetworkGraph(models.Model):
  user = models.ForeignKey(User)

  created  = models.DateTimeField(auto_now_add = True)
  modified = models.DateTimeField(auto_now = True)
  expired  = models.DateTimeField(null = True, blank = True)

  unique_id  = models.TextField()
  graph_data = models.TextField()
  shared = models.BooleanField(default=False)
  complete = models.BooleanField(default=False)

  class Meta:
    ordering = ["id"]
