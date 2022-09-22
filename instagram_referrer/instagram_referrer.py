from base64 import urlsafe_b64encode
import codecs
import datetime
from distutils.command.sdist import sdist
import json
import os
from instabot import Bot
from pickle import TRUE
from random import randint
import re
from time import sleep
import random_poem
from pathlib import Path
import string
import requests
import urllib.parse
from requests.utils import requote_uri
from instagram_referrer.random_city import random_city

from instagram_referrer.random_image import random_image

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)

# from .colors import colors
cwd =  os.getcwd()
settings_file_path = os.path.join(cwd, ".settings.json")
settings_file = Path(settings_file_path)
settings_file.touch(exist_ok=True)
random_cities  = random_city()
def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))

class InstagramReferrer():
    """+==============================+"""
    """|      Instagram Referrer      |"""
    """+==============================+"""
    this_last_email = (False, None)
    username:string = None
    password: string = None
    url: string = None
    api = None
    bot = None
    device_id = None
    proxy = None
    def __init__(self, username:string = None, password: string = None, url: string = None, proxy = None, use_bot=False, use_api=False) -> None:
        self.password = password
        self.url = url
        self.username = username
        self.api = None
        self.proxy = proxy
        if use_bot:
            self.bot_login()
        if use_api:
            self.api_login()
    def bot_login(self):
        try:
            self.bot = Bot()
            if not self.proxy:
              self.bot.login(username=self.username, password=self.password)
            else:
              self.bot.login(username=self.username, password=self.password, proxy=self.proxy)
        except Exception as ex:
            print("bot could not login:", ex)
    def api_login(self):
        try:
            if not os.path.isfile(settings_file):
                # settings file does not exist
                print('Unable to find file: {0!s}'.format(settings_file))
                # login new
                self.api = Client(
                    username = self.username, password = self.password,
                    on_login=lambda x: onlogin_callback(x, settings_file_path))
            else:
                with open(settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook=from_json)
                print('Reusing settings: {0!s}'.format(settings_file))
                self.device_id = cached_settings.get('device_id')
                # reuse auth settings
                self.api = Client(
                    self.username, self.password,
                    settings=cached_settings)
        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))
            # Login expired
            # Do relogin but use default ua, keys and such
            self.api = Client(
                self.username, self.password,
                device_id=self.device_id,
                on_login=lambda x: onlogin_callback(x, settings_file_path))
        cookie_expiry = self.api.cookie_jar.auth_expires
        print('Cookie Expiry: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))
    def get_shurtcut_from_api(self, debug_level: int = 0):  
            """ 
            +-> Posting the url into your account.
            +-> Creating a direct url to the post.
            """
            try:
                ## id: 47823396436
                photo_data = random_image.get_image(320,400)
                text = random_poem.get_poem()
                caption = f'{text} \n visit for more: {self.url}'
                # size = (1080,1350)
                size = (320,400)
                city = random_cities.get_city()
                locations = self.api.location_search(
                    latitude = city["lat"], 
                    longitude = city["lng"], 
                    query = city["name"]
                    )
                to_reel = True
                location = locations["venues"][randint(0, len(locations["venues"]))]
                print("\n\n\n", location)
                results = self.api.post_photo(photo_data, caption, size, to_reel)
                print("\n\n\n", results)
                return (True,self.password)
            except Exception as ex:
                return (False,None)
    def get_shurtcut_from_bot(self):
        list = self.bot.get_timeline_medias()
        # for li in list:
        #     print(li)
    def getshortcut(self):
        return requote_uri(f'https://l.instagram.com/?u={self.url}')
    def get_is_gd_link(self):
        URL = 'https://is.gd/create.php?format=simple&url={}'
        response = requests.get(URL.format(self.url))
        return response.text
    def get_chilp_it_link(self):
        URL = 'http://chilp.it/api.php?url={}'
        response = requests.get(URL.format(self.url))
        return response.text
    def get_urlz_fr_link(self):
        URL = 'https://urlz.fr/api_new.php?url={}'
        response = requests.get(URL.format(self.url))
        return response.text