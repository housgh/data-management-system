from django.db import models
from .entity import Entity

class Property(models.Model):
    entity= models.ForeignKey(Entity, on_delete=models.CASCADE, blank=True, null=True, related_name='properties')
    property_name = models.CharField(max_length=200)
    property_type = models.CharField(max_length=200)
    required = models.BooleanField()