from cStringIO import StringIO
import logging

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from requests.exceptions import ConnectionError
from sorl.thumbnail import default as sorl_default
from sorl.thumbnail.helpers import tokey
from sorl.thumbnail.shortcuts import get_thumbnail
import requests


logger = logging.getLogger(__name__)


def get_minecraft_avatar(minecraft_user, geometry_string, force=True):
    """
    This method uses the sorl-thumbnail cache backend to
    prevent images from being downloaded every time.
    It requires an username.
    """
    avatar_file = UploadedFile(
        file=StringIO(),
        name='%s/%s.png' % (settings.MEDIA_ROOT, tokey(minecraft_user)))

    try:
        # Check if the avatar is cached
        thumbnail = get_thumbnail(
            avatar_file, '100x100', quality=100, format='PNG')
    except IOError:
        download_thumbnail = True

    else:
        is_dummy = not hasattr(thumbnail, 'storage')
        if not is_dummy and not thumbnail.storage.exists(thumbnail.name):
            # It seems we have the avatar on cache (kvstore)
            # but it's not present on the storage
            download_thumbnail = True
            # Force remove thumbnail from kvstore
            sorl_default.kvstore.delete(thumbnail)
            # Log
            logger.warning('Avatar cache mismatch: %s (resetting)' % (
                minecraft_user,))
        else:
            logger.debug('Avatar fetched from cache: %s' % minecraft_user)
            download_thumbnail = False

    if download_thumbnail:
        logger.debug('Downloading avatar: %s' % minecraft_user)

        # Otherwise download avatar
        thumbnail = None

        try:
            skin_bin = requests.get(
                'http://s3.amazonaws.com/MinecraftSkins/%s.png' % (
                    minecraft_user
                )
            ).content
        except ConnectionError:
            return None

        try:
            skin = Image.open(StringIO(skin_bin)).convert('RGBA')
        except IOError:
            # Image not found or some permission error with S3
            if minecraft_user != 'char':
                if not force:
                    return None
                # Return default user avatar
                return settings.STATIC_URL + settings.DEFAULT_USER_AVATAR
        else:
            face = skin.crop((8, 8, 16, 16))
            accessories = skin.crop((40, 8, 48, 16))

            r, g, b, a = accessories.split()

            accessories = Image.merge('RGB', (r, g, b))
            mask = Image.merge('L', (a,))

            face.paste(accessories, (0, 0), mask)

            avatar = face.resize((135, 135))

            avatar.save(avatar_file, 'PNG')

            avatar_file.seek(0)

            # Save through sorl backend
            thumbnail = get_thumbnail(avatar_file, '100x100',
                                      quality=100, format='PNG')

    # Use the cached file
    return get_thumbnail(thumbnail, geometry_string,
                         quality=100, format='PNG').url
