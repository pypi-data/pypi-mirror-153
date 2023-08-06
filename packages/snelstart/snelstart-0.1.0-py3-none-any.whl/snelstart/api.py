import logging

import pandas as pd
import requests

from snelstart.core import Base


class SnelStart(Base):
    def __init__(self):
        super().__init__()
        self.max_retries = 5
        self.sec_wait = 10
        self.max_req_size = 500

    @staticmethod
    def check_allowed_module(module) -> None:
        allowed_modules = ["kostenplaatsen", "grootboekmutaties", "dagboeken", "grootboeken", "relaties"]

        if module not in allowed_modules:
            raise ValueError(f"No valid module given, choose from {', '.join(allowed_modules)}")

    def request_data(self, module, years: list = None, dataframe: bool = False):
        logging.info(f"Start requesting {module}")
        self.check_allowed_module(module)
        url = self.base_url + module
        json_list = []
        if module == "grootboekmutaties":
            if not years:
                raise ValueError("No years inserted while requesting grootboekmutaties")
            else:
                for year in years:
                    len_response = self.max_req_size
                    skip_count = 0
                    json_list = self.snelstart_requester(url, len_response, skip_count, json_list, year)
        else:
            len_response = self.max_req_size
            skip_count = 0
            json_list = self.snelstart_requester(url, len_response, skip_count, json_list)
        logging.info(f"Done with requesting of {module}")
        if dataframe:
            df = pd.DataFrame(json_list)
            return df
        else:
            return json_list

    def snelstart_requester(self, url, len_response, skip_count, json_list, year=None):
        while len_response == self.max_req_size:
            success = False
            retry = 1
            while not success:
                if retry > self.max_retries:
                    logging.warning(f"Max retries ({self.max_retries}) exceeded, stopping requests.")
                    break
                skip_value = skip_count * self.max_req_size
                if year:
                    logging.info(f"Year {year}: ")
                logging.info(f"Requesting data for endpoint {url}, and skip value {skip_value}")
                with requests.get(
                    url, headers=self.define_api_headers(), params=self.define_api_params(skip_value, year=year)
                ) as response:
                    if response:
                        json_data = response.json()
                        len_response = len(json_data)
                        success = True
                        json_list += json_data
                        skip_count += 1
                    else:
                        logging.info(f"No response, retrying in {self.sec_wait} seconds. Retry number: {retry}")
                        retry += 1
        return json_list

    def define_api_headers(self) -> dict:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
        }
        return headers

    @staticmethod
    def define_api_params(skip_value: int, year=None) -> dict:
        if year:
            params = {"$skip": f"{skip_value}", "$filter": f"year(Datum) eq {year}"}
        else:
            params = {"$skip": f"{skip_value}"}
        return params
