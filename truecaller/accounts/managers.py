# Django imports.
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, *arg, **kwargs):
        """Create and return a `User` with an phone_number, name and password."""

        name = kwargs.get('name', None)
        email = kwargs.get('email', None)
        phone_number = kwargs.get('phone_number', None)
        password = kwargs.get('password', None)

        if not phone_number:
            raise TypeError('Users must have a phone phone_number')

        if not password:
            raise TypeError('Users must have a password.')

        user = self.model(
            name = name,
            phone_number = phone_number,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, *args, **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions.
        """

        phone_number = kwargs.get('phone_number', None)
        if not phone_number:
            kwargs['phone_number'] = 7754938370

        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
