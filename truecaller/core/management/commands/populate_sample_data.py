# Built-in imports.
import json

# Django imports.
from django.core.management.base import BaseCommand

# App imports.
from accounts.models import User
from contacts.models import PersonalContacts
from accounts.serializers import UserRegisterSerializer


class Command(BaseCommand):
	help = "Management command for filling the db with sample data"

	def handle(self, *args, **kwargs):

		with open("sample_data.json") as json_file:
			sample_data = json.load(json_file)

		print('Filling db with sample data --------------------------------')

		sample_user = sample_data.get('user')
		sample_contacts = sample_data.get('contacts')

		try:
			# creating user
			user_serializer = UserRegisterSerializer(data=sample_user)
			user_serializer.is_valid(raise_exception=True)
			user_serializer.save()

			user_obj = User.objects.get(id=user_serializer.data.get('id'))

			for contact in sample_contacts:
				# creating personal contacts for the above user
				personal_contact_obj = PersonalContacts.objects.create(
					user=user_obj, phone_number=contact.get('phone_number'),
					name=contact.get('name'), email=contact.get('email'))
				personal_contact_obj.save()

			print('Success ------------------------------------------------------')

		except Exception as e:
			print(f'Something went wrong, error :- {e}')