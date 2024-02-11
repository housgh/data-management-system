from django.db import models
from .organization import Organization

class Entity(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    entity_name = models.CharField(max_length=30)