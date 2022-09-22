import string
import requests
class LinksReferrer():
    """+==============================+"""
    """|        links Referrer        |"""
    """+==============================+"""
    url: string = None
    def __init__(self, url: string ) -> None:
        self.url = url
    def getshortcuts(self):
        return [self.get_is_gd_link(), self.get_chilp_it_link(), self.get_chilp_it_link(), self.get_urlz_fr_link()]
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