import urllib2
import logging
import json

from .exceptions import MinecraftAuthenticationError


logger = logging.getLogger(__name__)


def authenticate(username, password):
    url = 'https://authserver.mojang.com/authenticate'

    payload = {
        'agent': {
            'name': 'Minecraft',
            'version': 1,
        },
        'username': username,
        'password': password,
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    try:
        request = urllib2.Request(url, json.dumps(payload), headers)
        response = urllib2.urlopen(request)

        try:
            response_payload = json.loads(response.read())

        finally:
            response.close()  # always close socket

        return response_payload

    except urllib2.HTTPError as e:
        raise MinecraftAuthenticationError(e)
