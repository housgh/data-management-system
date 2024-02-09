from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .organization import Organization

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)


def get_by_user_id(user_id):
    user = UserDetails.objects.filter(user_id=user_id)
    return user.first()
    