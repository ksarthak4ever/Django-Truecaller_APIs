# Django imports.
from django.urls import path

from accounts.views import UserRegisterView, UserLoginView


urlpatterns = [
    # Route to register users.
    path(r'register/', UserRegisterView.as_view(), name='user-register'),
    path(r'login/', UserLoginView.as_view(), name='user-login')

]