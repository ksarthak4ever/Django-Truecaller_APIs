# DRF imports.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

# App imports.
from accounts.models import User
from accounts.serializers import (
    UserRegisterSerializer, UserLoginSerializer
)


class UserRegisterView(APIView):
    """
    API to register user to Truecaller.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
    	req_data = request.data
    	phone_number = req_data.get('phone_number', None)
    	if User.objects.filter(phone_number=phone_number).exists():
    		return Response(
    			data="User with this phone number already exists",
    			status=status.HTTP_400_BAD_REQUEST
    		)
    	user_serializer = UserRegisterSerializer(data=req_data)
    	user_serializer.is_valid(raise_exception=True)
    	user_serializer.save()

    	return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API to login a registered user.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        req_data = request.data
        login_serializer = UserLoginSerializer(data=req_data)
        login_serializer.is_valid(raise_exception=True)

        return Response(data=login_serializer.data, status=status.HTTP_200_OK)