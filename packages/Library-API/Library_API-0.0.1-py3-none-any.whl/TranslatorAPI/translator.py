import json

import requests


class Translator:

    def __init__(self):
        self.url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
        self.headers = {
                "content-type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "application/gzip",
                "X-RapidAPI-Host": "google-translate1.p.rapidapi.com",
                "X-RapidAPI-Key": "9956beec72msh8f5b5e09b33da88p1d8b8cjsneac0d0fcdcea"
        }

    def translate_text(self, text, target_lang):
        payload = "q=" + text
        payload.replace(" ", "%20")
        payload.replace(",", "%2C")
        payload += ("&target=" + target_lang + "&source=en")
        response = requests.request("POST", self.url, data=payload, headers=self.headers)
        json_data = json.loads(response.text)
        formatted_string = json.dumps(json_data, indent=2)
        return formatted_string

