# Django imports.
from django.conf import settings
from django.contrib.auth import get_user_model

# DRF imports.
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import (
    get_authorization_header, BaseAuthentication
)

# Third party imports.
from jwt import decode as jwt_decode
from jwt.exceptions import DecodeError


class JWTAuthentication(BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request, regardless of
        whether the endpoint requires authentication.

        `authenticate` has two possible return values:

        1) `None` - We return `None` if we do not wish to authenticate. Usually
        this means we know authentication will fail. An example of
        this is when the request does not include a token in the
        headers.

        2) `(user, token)` - We return a user/token combination when
        authentication was successful.

        If neither of these two cases were met, that means there was an error.
        In the event of an error, we do not return anything. We simple raise
        the `AuthenticationFailed` exception and let Django REST Framework
        handle the rest.
        """

        request.user = None

        # `auth_header` should be an array with two elements:
        # 1) Name of the authentication header (in this case, "Token").
        # 2) JWT that we should authenticate against.
        auth_header = get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            return None  # Invalid token header. Don't attempt to authenticate.

        # The JWT library we're using can't handle the `byte` type, which is
        # commonly used by standard libraries in Python 3. To get around this,
        # we simply have to decode `prefix` and `token`. This does not make for
        # clean code, but it is a good decision because we would get an error
        # if we didn't decode these values.
        prefix, token = [i.decode('utf-8') for i in auth_header]

        if prefix.lower() != auth_header_prefix:
            # The auth header prefix is not what we expected. Do not attempt to
            # authenticate.
            return None

        # By now, we are sure there is a *chance* that authentication will
        # succeed. We delegate the actual credentials authentication to the
        # method below.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """

        try:
            payload = jwt_decode(token, settings.SECRET_KEY)
        except DecodeError:
            msg = 'Invalid authentication. Could not decode token.'
            raise AuthenticationFailed(msg)

        User = get_user_model()

        try:
            id_ = payload.get('id', None)
            user = User.objects.get(pk=id_)
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise AuthenticationFailed(msg)

        return (user, token)
