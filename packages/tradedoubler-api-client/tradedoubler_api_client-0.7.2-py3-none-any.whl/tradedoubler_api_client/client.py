import requests
import base64
import json
from tradedoubler_api_client.pending_sales import Pending_Sales
from tradedoubler_api_client.reporting import Reporting
from tradedoubler_api_client.exceptions import TradedoublerConnectionError, TradedoublerRateLimitExceeded
# https://advertiserwip.docs.apiary.io/
# dokumentacja tego gówna
# luźno powiązana z rzeczywostością


class Tradedoubler:
    def __init__(self, credentials_path, print_mode=False):
        credentials = self.__open_credentials(credentials_path)
        self.td_secret = credentials['td_secret']
        self.td_id = credentials['td_id']
        self.td_user_name = credentials['td_user_name']
        self.td_userpassword = credentials['td_userpassword']
        self.athu = self.__get_auth_token()
        self.print_mode = print_mode

    @staticmethod
    def __open_credentials(credentials_path):
        with open(credentials_path) as f:
            return json.load(f)

    def __get_auth_token(self):
        auth_bytes = f'{self.td_id}:{self.td_secret}'.encode('ascii')
        auth_code = base64.b64encode(auth_bytes)
        return auth_code.decode('ascii')

    def __get_bearer(self):
        values = f'start&grant_type=password&username={self.td_user_name}&password={self.td_userpassword}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.athu}'
        }
        r = requests.post('https://connect.tradedoubler.com/uaa/oauth/token', data=values, headers=headers)
        self.handle_errors(r)
        return r.json()["access_token"]

    def get_request_header(self, content_type='application/json'):
        return {
            'Content-Type': content_type,
            'Authorization': f'Bearer {self.__get_bearer()}'
        }

    def handle_errors(self, req):
        if req.status_code == 200:
            pass
        elif req.status_code == 429:
            raise TradedoublerRateLimitExceeded(f'{req.status_code} - {req.text}\n\n{req.url}')
        elif req.status_code != 200:
            raise TradedoublerConnectionError(f'{req.status_code} - {req.text}\n\n{req.url}')

    def get_my_user_details(self):
        r = requests.get('https://connect.tradedoubler.com/usermanagement/users/me', headers=self.get_request_header())
        self.handle_errors(r)
        return r.json()

    def pending_sales(self):
        return Pending_Sales(self)

    def reporting(self):
        return Reporting(self)
