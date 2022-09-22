# import json
# from instagram_referrer import InstagramReferrer, random_image, random_city
from distutils.command.sdist import sdist
from instagram_referrer import InstagramReferrer, random_image, random_city
import requests
Referral = InstagramReferrer(url="https://youtu.be/ubVJ8OARMxs")
print(Referral.get_is_gd_link())
print(Referral.get_chilp_it_link())
print(Referral.get_chilp_it_link())
