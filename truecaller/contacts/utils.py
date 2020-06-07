# Django imports.
from django.db.models import Q # using Q objects for complex lookups

# App imports.
from accounts.models import User
from contacts.models import PersonalContacts
from contacts.serializers import (
	UserContactSerializer,
	PersonalContactsSerializer
)


def search_contacts_for_name(searched_name):
	# as there can be more than one user/contact
	# with same name or parts of same name
    users_qs = User.objects.filter(
        Q(name__startswith = searched_name)|
        Q(name__icontains = searched_name)
    ).distinct()
    contacts_qs = PersonalContacts.objects.filter(
        Q(name__startswith = searched_name)|
        Q(name__icontains = searched_name)
    ).distinct()
    users_serializer = UserContactSerializer(users_qs,many=True)
    contacts_serializer = PersonalContactsSerializer(contacts_qs, many=True)
    final_data=dict(
    	registered_users = users_serializer.data,
        personal_contacts = contacts_serializer.data
    )
    return final_data


def search_contacts_for_number(searched_number):
	# searching for person in registered users
    user_qs = User.objects.filter(phone_number=searched_number)
    if user_qs.exists():
    	# as there can be only 1 registered user with a number
    	person = user_qs.first()
    	user_serializer = UserContactSerializer(person)
    	return user_serializer.data 
    else:
        contacts_qs = PersonalContacts.objects.filter(
        					phone_number=searched_number
        				)
        if contacts_qs.exists():
            serializer = PersonalContactsSerializer(contacts_qs, many=True)
            final_data= dict(
				message="An unregistered contact number",
                data=serializer.data
            )
            return final_data
        return dict()