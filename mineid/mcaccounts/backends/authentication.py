from django.contrib.auth import get_user_model

from ..authenticate import authenticate
from ..models import MinecraftAccount
from ..utils import create_minecraft_user
from ..exceptions import UserAlreadyExists


User = get_user_model()


class MinecraftBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            response = authenticate(username, password)
        except:
            return None
        else:
            # Append other profiles
            profiles = response.get('availableProfiles')

            if profiles:
                # Add selected profile
                selected_profile_id = response.get('selectedProfile').get('id')

                all_profiles_ids = [p.get('id') for p in profiles]

                mc_account = MinecraftAccount.objects.filter(
                    profile_id__in=all_profiles_ids
                ).first()
            else:
                mc_account = None
                selected_profile_id = None

            if not mc_account:
                return create_minecraft_user(username, profiles,
                                             primary=selected_profile_id)
            else:
                return mc_account.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
