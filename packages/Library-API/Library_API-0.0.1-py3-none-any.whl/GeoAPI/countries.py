import json

import requests


class Countries:

    def __init__(self):
        self.url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/"
        self.headers = {
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            "X-RapidAPI-Key": "9956beec72msh8f5b5e09b33da88p1d8b8cjsneac0d0fcdcea"
        }

    def get_country_details(self, country_id):
        new_url = self.url + country_id
        response = requests.request("GET", new_url, headers=self.headers)
        json_data = json.loads(response.text)
        formatted_string = json.dumps(json_data, indent=2)
        return formatted_string

    def get_region_details(self, country_id, region_id):
        new_url = self.url + country_id + "/regions/" + region_id
        response = requests.request("GET", new_url, headers=self.headers)
        json_data = json.loads(response.text)
        formatted_string = json.dumps(json_data, indent=2)
        return formatted_string

