import requests
import json 

def check_license(license: str, hwid: str):
     payload = json.dumps({"user_license": license, "user_hwid": hwid})
     reponse = requests.post("http://159.65.28.35:8000/api/license", data=payload)

     if reponse.status_code != 200:
          return True
     else:
          return False      