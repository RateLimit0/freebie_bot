import json

def check_files():
     try:
          with open("proxies.txt", "r") as f:
               if f.read() == "":
                    with open("proxies.txt", "w") as f:
                         f.write("localhost")
     except FileNotFoundError:
          print("[ERROR] Proxy File Not Found, Adding")
          with open("proxies.txt", "w") as f:
               f.write("localhost")

     try:
          with open("settings.json", "r") as f:
               json_data = f.read()
               if json_data == "":
                    with open("settings.json", "w") as f:
                         json.dump(
                         {
                              "catchall": "@example.com",
                              "address": {
                                   "house_number": "",
                                   "line_1": "",
                                   "line_2": "",
                                   "town/city": "",
                                   "province/state/county": "",
                                   "postcode": "",
                                   "country_code": "GB"
                              }
                         }, f)
     except FileNotFoundError:
          print("[ERROR] Settings File Not Found, Adding")
          with open("settings.json", "w") as f:
               json.dump(
               {
                    "catchall": "@example.com",
                    "address": {
                         "house_number": "",
                         "line_1": "",
                         "line_2": "",
                         "town/city": "",
                         "province/state/county": "",
                         "postcode": "",
                         "country_code": "GB"
                    }
               }, f)                    