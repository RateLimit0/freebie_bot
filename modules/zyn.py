import aiohttp
import string 
import random
import json 
import asyncio
from utils.misc import random_number, Print
from utils.jigg import fake_name, jigged_house_num, jigged_address, jigged_line_2
from utils.proxies import proxy, check_proxy
from utils.webhook import webhooks

class main: 
     def __init__(self, product_id):
          self.cookie_store = aiohttp.CookieJar()
          self.account_payload = {
               "customerName": "",
               "customerEmail": "",
               "confirmCustomerEmail": "",
               "customerPassword": "",
               "confirmPassword": "",
               "presentSetId": 11,
               "referrerCode": "",
               "OptInReceiveNewsLetterRadio": False,
               "returnTo": "" ,
               "isLinkingAccounts": "",
               "accountLinkingCsrfToken": ""
          }

          self.headers = {
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "accept-encoding": "gzip, deflate, br",
               "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
               "cache-control": "no-cache",
               "content-type": "application/x-www-form-urlencoded",
               "pragma": "no-cache",
               "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
               "sec-ch-ua-mobile": "?0",
               "sec-ch-ua-platform": '"Windows"',
               "sec-fetch-dest": "document",
               "sec-fetch-mode": "navigate",
               "sec-fetch-site": "same-origin",
               "sec-fetch-user": "?1",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"    
          }

          self.product_id = product_id
          self.fake_name = fake_name()
          self.check_proxy = check_proxy()
          self.proxies = []

          with open("settings.json", "r") as f:
               self.settings = json.load(f)

          self.address = self.settings["address"]
          self.catchall = self.settings["catchall"]

          self.jigged_house_num = jigged_house_num(self.address["house_number"])
          self.jigged_address = jigged_address(self.address["line_1"])
          self.jigged_line_2 = jigged_line_2(self.address["line_2"], self.address["house_number"])
          self.city = self.address["town/city"]
          self.state = self.address["province/state/county"]
          self.postcode = self.address["postcode"]
          self.country_code = self.address["country_code"]

          self.order_payload = {"fullName":"","payerName":"","contactNumber":"","deliveryAddress":{"addressType":"postal","addressee":"","organisationName":"","buildingNameNumber":"","line1":"","line2":"","line3":"","line4":"","postcode":"","countryCode":""},"payment":{"method":"credit","consentToReuse":"null"},"deliverySelection":{"groupSelections":[{"deliveryOptionType":1, "groupId":0, "subDeliveryOptionIndex":"null","used":True}],"deliveryOptionsRequest":{"country":"","postCode":"","state":"","townCity":""}},"consentGiven":True,"reCaptchaToken":"","deviceInformation":{"deviceId":"4ad2ff8fa0959d5b5a27e6bf8b45fb99","screenResolution":{"width":"1440","height":"2560","ratio":"1"},"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36","timezone":"Europe/London","language":"en-GB","acceptHeader":"application/json","colorDepth":"24","timeZoneOffset":"-60","javaEnabled":False}}

          self.delivery_payload = {"country":"GB","postCode":"TN25 4QS","state":"","townCity":""}     

          if "@" not in self.catchall:
               self.catchall = f"@{self.catchall}" 

          self.random_email = "".join(random.choice(string.ascii_lowercase) for i in range(10)) + self.catchall
          self.random_password = "".join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for i in range(10))
          self.account_payload.update({'customerEmail': self.random_email})
          self.account_payload.update({'confirmCustomerEmail': self.random_email})
          self.account_payload.update({'customerPassword': self.random_password})
          self.account_payload.update({'confirmPassword': self.random_password})
          self.account_payload.update({'customerName': self.fake_name})

          self.delivery_payload.update({'country': self.country_code})
          self.delivery_payload.update({'postCode': self.postcode})
          self.delivery_payload.update({'townCity': self.city})
          self.delivery_payload.update({'state': self.state})

          self.order_payload.update({'fullName': self.fake_name})
          self.order_payload.update({'contactNumber': "07" + str(random.randint(100000000, 999999999))})
          self.order_payload.update({'deliveryAddress': {'addressType': 'postal', 'addressee': self.fake_name, 'organisationName': '', 'buildingNameNumber': self.jigged_house_num, 'line1': self.jigged_address, 'line2': f'{self.jigged_line_2}', 'line3': self.city, 'line4': self.state, 'postcode': self.postcode, 'countryCode': self.country_code}})
          self.order_payload.update({"deliveryOptionsRequest": {"country": self.country_code, "postCode": self.postcode}})

     async def zyn(self):
          while True: 
               try:
                    async with aiohttp.ClientSession(headers=self.headers, trust_env=True) as s:
                         Print.default("Fetching Session On https://uk.zyn.com/")
                         if self.check_proxy == True:
                              self.proxies.append(proxy())
                              self.check_proxy = True
                         else:
                              self.check_proxy = False     
                         
                         if self.check_proxy == True: 
                              get_site = await s.get('https://uk.zyn.com/accountCreate.account', proxy=self.proxies[0])
                         else:
                              get_site = await s.get('https://uk.zyn.com/accountCreate.account')

                         if get_site.status != 200:
                              return None

                         Print.default("Fetching CSRF")
                         csrf_token = get_site.cookies['csrf_token'].value
                         self.account_payload.update({'csrfToken': csrf_token})

                         Print.default("Creating Account")
                         if self.check_proxy == True:
                              create_account = await s.post('https://uk.zyn.com/accountCreate.account', data=self.account_payload, proxy=self.proxies[0])
                         else:
                              create_account = await s.post('https://uk.zyn.com/accountCreate.account', data=self.account_payload)

                         if create_account.status != 200:
                              Print.red("Failed To Create Account")
                              return None

                         Print.default(f"Adding {self.product_id} To Basket")
                         if self.check_proxy == True:
                              add_cart = await s.get(f"https://uk.zyn.com/basketinterface.json?productId={self.product_id}&siteId=236&siteDefaultLocale=en_GB&siteSubsiteCode=en&variationLength=0&quantity=1&fromWishlist=false", proxy=self.proxies[0])
                         else:
                              add_cart = await s.get(f"https://uk.zyn.com/basketinterface.json?productId={self.product_id}&siteId=236&siteDefaultLocale=en_GB&siteSubsiteCode=en&variationLength=0&quantity=1&fromWishlist=false")

                         if add_cart.status != 200:
                              Print.red("Failed To Add To Basket")
                              return None
                         
                         cart_json = await add_cart.json()
                         #print(cart_json)

                         if cart_json['simpleBasket']["basketItems"][0]["quantity"] != 1:
                              Print.red("Failed to add to cart")
                              return None                    

                         Print.default("Adding Discount Code")
                         if self.check_proxy == True:
                              add_discount = await s.post("https://uk.zyn.com/my.basket", data={"discountCode": "Q3FREESAMPLE"}, proxy=self.proxies[0])
                         else:
                              add_discount = await s.post("https://uk.zyn.com/my.basket", data={"discountCode": "Q3FREESAMPLE"})

                         if add_discount.status != 200:
                              Print.red("Failed To Add Discount Code")
                              return None

                         Print.default("Starting Checkout")
                         if self.check_proxy == True:
                              start_checkout = await s.post("https://uk.zyn.com/checkoutStart.account", proxy=self.proxies[0])
                         else:
                              start_checkout = await s.post("https://uk.zyn.com/checkoutStart.account")

                         if start_checkout.status != 200:
                              Print.red("Failed To Start Checkout")
                              return None
                         checkout_url = str(start_checkout.url) 
                         while True:
                              if self.check_proxy == True:
                                   checkout = await s.get(checkout_url, proxy=self.proxies[0])
                              else:
                                   checkout = await s.get(checkout_url)

                              try:
                                   session_cookie = checkout.cookies['nc_s'].value
                                   break
                              except KeyError:
                                   Print.red("Failed To Get Session Cookie, retrying")
                                   await asyncio.sleep(1.5)
                                   
                         self.headers.update({"content-type": "application/json; charset=utf-8"})
                         self.headers.update({"Referer": checkout_url})
                         self.headers.update({"x-thg-client": "checkout-web-js"})
                         self.headers.update({"sessionId": session_cookie})

                         while True:
                              if self.check_proxy == True:
                                   delivery = await s.post("https://checkout.uk.zyn.com/checkout-api/v2/delivery", data=json.dumps(self.delivery_payload), headers=self.headers, proxy=self.proxies[0])
                              else:
                                   delivery = await s.post("https://checkout.uk.zyn.com/checkout-api/v2/delivery", data=json.dumps(self.delivery_payload), headers=self.headers)

                              if delivery.status != 202:
                                   break
                              else:
                                   Print.red("Failed To Set Delivery Options, retrying")
                                   await asyncio.sleep(1.5)

                         Print.default("Placing Order")
                         if self.check_proxy == True:
                              order_product = await s.post("https://checkout.uk.zyn.com/checkout-api/v2/order/place-order", data=json.dumps(self.order_payload), headers=self.headers, proxy=self.proxies[0])
                         else:
                              order_product = await s.post("https://checkout.uk.zyn.com/checkout-api/v2/order/place-order", data=json.dumps(self.order_payload), headers=self.headers)     

                         if order_product.status != 202:
                              Print.red("Failed To Place Order")
                              return None
                         
                         if self.check_proxy == True:
                              order_status = await s.get("https://checkout.uk.zyn.com/checkout-api/v2/order/status", headers=self.headers, proxy=self.proxies[0])
                         else:
                              order_status = await s.get("https://checkout.uk.zyn.com/checkout-api/v2/order/status", headers=self.headers)

                         if order_status.status != 200:
                              Print.red("Failed To Place Order")
                              return None
                         else:
                              Print.green("Order Placed!")
                              break

               except aiohttp.client_exceptions.ClientHttpProxyError:
                    Print.red("Proxy Error, Rotating Proxy")
                    if self.check_proxy == True:
                         self.proxies.clear()
                         self.proxies.append(proxy())
               except aiohttp.client_exceptions.ServerDisconnectedError:  
                    Print.red("Server Disconnected, Retrying")         
                    if self.check_proxy == True:
                         self.proxies.clear()
                         self.proxies.append(proxy())
               except Exception:
                    if self.check_proxy == True:
                         self.proxies.clear()
                         self.proxies.append(proxy())     