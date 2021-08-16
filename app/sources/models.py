from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from config import settings


class Source(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=50)
    source_value = models.DecimalField(max_digits=9, decimal_places=2)
    
    def __str__(self):
        return self.source_name
