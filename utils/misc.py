from colorama import Fore
from faker import Faker
import random
from datetime import datetime
import os
p = print


def random_number(start, end):
     return random.randint(start, end)

title = """
███╗   ██╗██╗████████╗████████╗██╗   ██╗     █████╗ ██╗ ██████╗ 
████╗  ██║██║╚══██╔══╝╚══██╔══╝╚██╗ ██╔╝    ██╔══██╗██║██╔═══██╗
██╔██╗ ██║██║   ██║      ██║    ╚████╔╝     ███████║██║██║   ██║
██║╚██╗██║██║   ██║      ██║     ╚██╔╝      ██╔══██║██║██║   ██║
██║ ╚████║██║   ██║      ██║      ██║       ██║  ██║██║╚██████╔╝
╚═╝  ╚═══╝╚═╝   ╚═╝      ╚═╝      ╚═╝       ╚═╝  ╚═╝╚═╝ ╚═════╝ 
"""

def clear():
     os.system('cls')

def time_stamp():
     return str(datetime.utcnow().strftime(("%H:%M:%S.%f")))

class Print:
     def default(content: str):
          p(f"[{time_stamp()}] {content}")

     def red(content: str):
          p(Fore.RED + f"[{time_stamp()}] {content}" + Fore.RESET)   

     def green(content: str):
          p(Fore.GREEN + f"[{time_stamp()}] {content}" + Fore.RESET)

     def yellow(content: str):
          p(Fore.YELLOW + f"Print {content}" + Fore.RESET)  

     def title():
          p(title)