from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from registration.forms import RegistrationForm

from ..mcaccounts.exceptions import UserAlreadyExists


User = get_user_model()


class RegistrationForm(RegistrationForm):
    """ Note: These forms were inherited only to remove
        the username dependency
    """
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['username']


class RegistrationFormUniqueEmail(RegistrationForm):
    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _(
                    "This email address is already in use. "
                    "Please supply a different email address."
                ))
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super(RegistrationFormUniqueEmail, self).clean()
        cleaned_data['username'] = cleaned_data.get('email')
        return cleaned_data


class EmailAddressForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class AuthenticationForm(AuthenticationForm):
    def clean(self):
        try:
            return super(AuthenticationForm, self).clean()
        except UserAlreadyExists:
            raise forms.ValidationError(
                _(
                    "We could not associate your Minecraft account because "
                    "this email address is already associated with another "
                    "account."
                ))
