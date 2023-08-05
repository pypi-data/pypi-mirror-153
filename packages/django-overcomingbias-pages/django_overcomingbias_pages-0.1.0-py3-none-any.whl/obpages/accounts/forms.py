from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, UsernameField

import obpages.accounts.tasks
from obpages.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email Address")

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField}


class CustomPasswordResetForm(PasswordResetForm):
    """Custom reset form which uses Huey to send email."""

    def send_mail(self, *args, **kwargs):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        obpages.accounts.tasks.send_mail(*args, **kwargs)
