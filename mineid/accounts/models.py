from .abstract_models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    objects = UserManager()

    def get_api_dict(self, base_url):
        data = {}
        data['email'] = self.email

        minecraft_account = self.minecraft_accounts.primary()
        
        if minecraft_account:
            minecraft_account_data = minecraft_account.get_api_dict(base_url)
            data['primary_profile'] = minecraft_account_data

        return data
