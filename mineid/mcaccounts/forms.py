from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import MinecraftAccount
from .authenticate import authenticate

class MinecraftAccountForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(
        label=_('Password'),
        help_text=_('Your password will not be stored in our database'),
        widget=forms.PasswordInput)

    class Meta:
        fields = ()

    def __init__(self, *args, **kwargs):
        super(MinecraftAccountForm, self).__init__(*args, **kwargs)
        self.profiles = []

    def clean(self):
        cleaned_data = super(MinecraftAccountForm, self).clean()

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            response = authenticate(username, password)
        except:
            raise forms.ValidationError(_(
                'You entered invalid credentials. '
                'Username or password are incorrect.'))
        else:
            selected_profile = response.get('selectedProfile')

            # Add selected profile
            profile_id = selected_profile.get('id')

            try:
                MinecraftAccount.objects.get(profile_id=profile_id)
            except MinecraftAccount.DoesNotExist:
                self.profiles.append(selected_profile)
            else:
                raise forms.ValidationError(_(
                    'This Minecraft Profile is already being used '
                    'by another account.'))

            # Append other profiles
            for other_profile in response.get('availableProfiles'):
                if other_profile.get('id') != profile_id:
                    self.profiles.append(other_profile)

        return cleaned_data

    def save(self, user):
        is_first_profile = not user.minecraft_accounts.exists()

        # Save profiles
        for order, profile in enumerate(self.profiles):
            primary = is_first_profile and order == 0
            MinecraftAccount.objects.create(
                user=user,
                profile=profile.get('name'),
                profile_id=profile.get('id'),
                primary=primary,
            )
