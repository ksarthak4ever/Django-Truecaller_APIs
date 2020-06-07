from django.db import models
from accounts.models import User


class PersonalContacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    spam_count = models.IntegerField(default=0)
    email = models.EmailField(max_length=75, null=True, blank=True)
    
    def __str__(self):
        return self.name