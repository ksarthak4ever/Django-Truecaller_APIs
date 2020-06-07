# Django imports.
from django.contrib.auth import authenticate


# DRF imports.
from rest_framework.serializers import (
    # Serializers.
    Serializer, ModelSerializer,

    # Fields.
    CharField, IntegerField, UUIDField, BooleanField,

    # Errors.
    ValidationError,
)

# App imports.
from accounts.models import User


class UserRegisterSerializer(ModelSerializer):
    """Serializers signup requests and creates a new user."""

    u_id = UUIDField(read_only=True)

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = CharField(max_length=128, min_length=8, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:  
            # Iterate over the serializer fields.
            # Set the custom error message.
            self.fields[field].error_messages['required'] = \
                f'Field `{field}` is required for `user` data.'

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = (
            'id', 'u_id', 'name', 'phone_number', 'email', 'password',
            'spam_count', 'token',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(Serializer):
    id_ = IntegerField(read_only=True)
    u_id = UUIDField(read_only=True)
    name = CharField(read_only=True)
    phone_number = CharField(max_length=15)
    email = CharField(max_length=255, required=False)
    token = CharField(max_length=255, read_only=True)
    password = CharField(max_length=128, write_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided a phone number
        # and password and that this combination matches one of the users in
        # the database.
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)

        # Raise an exception if phone number is not provided.
        if not phone_number:
            raise ValidationError("Phone number is required to log in")

        # Raise an exception if the password is not provided.
        if not password:
            raise ValidationError("Password is required to log in")

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this phone_number/password combination. Notice how
        # we pass `phone_number` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `phone_number`.
        user = authenticate(username=phone_number, password=password)

        # If no user was found matching this phone_number/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if not user:
            raise ValidationError(
                'user with this email and password was not found'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise ValidationError('this user has been deactivated')

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.

        return dict(
            id_=user.id, u_id=user.u_id, name=user.name,
            phone_number=user.phone_number, email=user.email, 
            spam_count=user.spam_count, token=user.token,
        )