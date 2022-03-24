'''
Author : Kishor Ponnaganti (kishor.ponnaganti@gmail.com)
Submitted for Kraken Code Assesment
Date : 20-March-2022
'''

import requests


class api_call(object):
    response = {}

    def __init__(self):
        self.uri = 'https://api.kraken.com'
        self.version = '0'
        self.session = requests.Session()
        self.response = None

    def api_endpt(self, method, data=None):
        if data is None:
            data = {}

        krak_endpt = self.uri + '/' + self.version + '/public/' + method
        self.response = self.session.post(krak_endpt, data=data)
        return self.response
