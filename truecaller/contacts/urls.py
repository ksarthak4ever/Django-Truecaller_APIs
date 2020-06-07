# Django imports.
from django.urls import path

from contacts.views import (
	SetSpamContactView, 
	ContactSearchView,
	UserDetailProfileView, 
)


urlpatterns = [
	# Route to set a number as spam.
    path(r'spam/', SetSpamContactView.as_view(), name='set-spam'),
    # Route to search a person based on the name or number.
    path(r'search/', ContactSearchView.as_view(), name='contact-search'),
    # Route to fetch details of a specific registered user or contact.
    path(r'detail/<int:user_id>/', UserDetailProfileView.as_view(), name='detailed-view')

]