from modules.zyn import main
from utils.files import check_files
from utils.misc import title, clear
from utils.webhook import webhooks
import asyncio 
import logging
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
logging.getLogger('asyncio').setLevel(logging.CRITICAL)

tasks = []

async def run():
     await asyncio.gather(*tasks)

def menu():
     print(title)
     check_files()
     clear()
     print(title)
     print("[0] Zyn")
     print("[1] Exit")

     i = input("Enter Option: ")

     if i == "0":
          product_sku = input("Enter Product Link Or SKU: ")
          if "https" in product_sku:
               product_sku = product_sku.split("/")
               product_sku = product_sku[4]
               if ".html" in product_sku:
                    product_sku = product_sku.replace(".html","")

          tasks_input = input("Number Of Tasks: ")   
          for _ in range(int(tasks_input)):
               tasks.append(asyncio.ensure_future(*[main(int(product_sku)).zyn()]))

          clear()
          print(title)
          print("Starting Zyn Tasks")
          asyncio.get_event_loop().run_until_complete(run())     
     elif i == "1":
          exit()


menu()