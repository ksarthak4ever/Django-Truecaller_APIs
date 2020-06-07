# DRF imports.
from rest_framework import serializers

# App imports.
from accounts.models import User
from contacts.models import PersonalContacts


class UserContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'name', 'phone_number', 'spam_count')


class PersonalContactsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PersonalContacts
        fields = ('id', 'name', 'phone_number', 'spam_count')
