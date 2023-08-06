import json
import logging
import os

import requests


class Base:
    def __init__(self):
        self.api_version = "v2"
        self.base_url = f"https://b2bapi.snelstart.nl/{self.api_version}/"
        self.client_key = os.environ.get("SNELSTART_CLIENT_KEY")
        self.subscription_key = os.environ.get("SNELSTART_SUBSCRIPTION_KEY")
        self.access_token = self.set_access_token()

    def set_access_token(self):

        service_url = "https://auth.snelstart.nl/b2b/token"
        response = requests.post(service_url, data={"grant_type": "clientkey", "clientkey": self.client_key})
        if response:
            json_data = json.loads(response.text)
            access_token = json_data.get("access_token")
            logging.info("obtained access token.")
        else:
            access_token = None
            logging.info(response.text)

        return access_token
