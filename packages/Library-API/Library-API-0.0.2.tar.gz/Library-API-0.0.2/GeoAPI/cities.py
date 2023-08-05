import json

import requests

class Cities:

	def __init__(self):
		self.url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/"
		self.headers = {
			"X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
			"X-RapidAPI-Key": "9956beec72msh8f5b5e09b33da88p1d8b8cjsneac0d0fcdcea"
		}


	def get_city_details(self, city_id):
		new_url = self.url + city_id
		response = requests.request("GET", new_url, headers=self.headers)
		json_data = json.loads(response.text)
		formatted_string = json.dumps(json_data, indent=2)
		return formatted_string

	def get_current_time(self, city_id):
		new_url = self.url + city_id + "/time"
		response = requests.request("GET", new_url, headers=self.headers)
		json_data = json.loads(response.text)
		formatted_string = json.dumps(json_data, indent=1)
		return formatted_string


