from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from .models import MinecraftAccount
from .exceptions import UserAlreadyExists


User = get_user_model()


def create_minecraft_user(username, profiles, primary):
    try:
        validate_email(username)
    except ValidationError:
        email = None
    else:
        email = username

    # This user can only log in through Minecraft
    # authentication backend
    user = User(username=username, email=email)
    user.set_unusable_password()

    try:
        user.save()
    except IntegrityError:
        raise UserAlreadyExists

    # Save profiles
    for profile in profiles:
        MinecraftAccount.objects.create(
            user=user,
            profile=profile.get('name'),
            profile_id=profile.get('id'),
            primary=primary,
        )

    return user
