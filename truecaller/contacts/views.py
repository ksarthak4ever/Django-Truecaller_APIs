# Django imports.
from django.db.models import Q # using q objects for complex lookups

# DRF imports.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# App imports.
from accounts.models import User
from contacts.models import PersonalContacts
from contacts.serializers import (
	UserContactSerializer,
	PersonalContactsSerializer
)
from contacts.utils import (
	search_contacts_for_name,
	search_contacts_for_number
)


class SetSpamContactView(APIView):
	"""
	API to set a specific user/contact or number as spam.
	"""
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		req_data = request.data
		phone_number = req_data.get('phone_number', None)
		if not phone_number:
			return Response(
				data = "Phone number is needed to set as spam",
				status = status.HTTP_400_BAD_REQUEST
			)

		registered_user_qs = User.objects.filter(
			phone_number = phone_number
		)
		personal_contacts_qs = PersonalContacts.objects.filter(
			phone_number = phone_number
		)

		if registered_user_qs.exists():
			# if number belongs to a registered user
			registered_user_obj = registered_user_qs.first()
			if request.user == registered_user_obj:
				# as a registered user can't report themselves as spam
				return Response(
					data="Registered users can't report themselves as spam",
					status=status.HTTP_400_BAD_REQUEST
				)
			registered_user_obj.spam_count += 1
			registered_user_obj.save()
			serializer = UserContactSerializer(registered_user_obj)
			return Response(data=serializer.data, status=status.HTTP_200_OK)

		elif personal_contacts_qs.exists():
			# if number belongs to a user or user's contact
			for contact in personal_contacts_qs:
				contact.spam_count += 1
				contact.save()
			serializer = PersonalContactsSerializer(personal_contacts_qs, many=True)
			return Response(data=serializer.data, status=status.HTTP_200_OK)

		else:
			# in case of random number
			# adding the number as a personal contact with no user
			# and setting the spam count for it as 1
			spam_number_obj = PersonalContacts.objects.create(
				phone_number=phone_number,
				spam_count=1
			)
			serializer = PersonalContactsSerializer(spam_number_obj)
			return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ContactSearchView(APIView):
	"""
	API to search for a person based on their
	name or phone number.
	"""
	permission_classes = (IsAuthenticated, )

	def get(self, request):
		req_data = request.GET
		name = req_data.get('name', None)
		phone_number = req_data.get('phone_number', None)

		if name:
			final_data = search_contacts_for_name(name)
		elif phone_number:
			final_data = search_contacts_for_number(phone_number)
		else:
			# person not found. 
			return Response(data=[],status=status.HTTP_200_OK)

		return Response(data=final_data, status=status.HTTP_200_OK)


class UserDetailProfileView(APIView):
	"""
	API to fetch details of a specific search result 
	i.e all details along with spam likelihood
	"""
	permission_classes = (IsAuthenticated, )

	def get(self, request, user_id=None):

		registered_user_qs = User.objects.filter(id=user_id)
		if registered_user_qs.exists():
			searched_user_obj = registered_user_qs.first()
			searched_user_serializer = UserContactSerializer(searched_user_obj)
			final_data = searched_user_serializer.data

			# checking if selected user is registered
			# and in contact list of authenticated user
			auth_user = request.user
			auth_user_number = auth_user.phone_number
			contact_connection_check_qs = PersonalContacts.objects.filter(
				Q(user=searched_user_obj) &
				Q(phone_number__icontains=auth_user_number)
			)

			if contact_connection_check_qs:
				# if user is registered and in contact list
				final_data['email'] = searched_user_obj.email

			return Response(data=final_data, status=status.HTTP_200_OK)

		contacts_qs = PersonalContacts.objects.filter(id=user_id)
		if contacts_qs.exists():
			contacts_serializer = PersonalContactsSerializer(contacts_qs.first())
			
			return Response(data=contacts_serializer.data, status=status.HTTP_200_OK)

		return Response(data="No user/contact found for this id", status=status.HTTP_400_BAD_REQUEST)
