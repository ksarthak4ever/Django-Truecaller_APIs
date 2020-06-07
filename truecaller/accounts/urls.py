# Django imports.
from django.urls import path

# App imports.
from accounts.views import UserRegisterView, UserLoginView


urlpatterns = [
    # Route to register users.
    path(r'register/', UserRegisterView.as_view(), name='user-register'),
    # Route to login registered users.
    path(r'login/', UserLoginView.as_view(), name='user-login')

]