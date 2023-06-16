from django import forms
from django.contrib.auth.models import User
from django.core import validators

from . import models


class MainModelForm(forms.ModelForm):
    class Meta:
        model = models.MainModel
        fields = '__all__'


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'username',
            # 'first_name',
            # 'last_name',
            'email',
            # 'is_active',
            # 'is_staff',
            # 'is_superuser',
            # 'password',
            # 'last_login',
            # 'groups',
            # 'user_permissions',
            # 'date_joined',
        ]


def validate_list_of_emails(value):
    values = value.strip().splitlines()
    values = [value.strip() for value in values]
    values = [value for value in values if value]
    for value in values:
        validators.validate_email(value)
    return values


def null_validator():
    print('null_validator')


class TextFieldListOfEmailAddressesField(forms.CharField):
    widget = forms.Textarea()
    default_validators = [
        validate_list_of_emails,
        null_validator,
    ]
    def clean(self, value):
        # because we are overriding clean, no other validators - including default - are executed
        return validate_list_of_emails(value)


class CreateUsersForm(forms.Form):
    email_addresses = TextFieldListOfEmailAddressesField(
        widget=forms.Textarea(),
        required=False,
        help_text='Email addresses pre-existing or duplicates are ignored.',
        label='Add users by providing a list of email addresses:',
    )
