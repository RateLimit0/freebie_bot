from faker import Faker
import random
from utils.misc import random_number
import string


def fake_name():
     fake = Faker()
     return fake.name()

def jigged_house_num(house_num: str):
     for _ in range(random_number(1,5)):
          jigged_house_num = ''.join(('0',house_num,''))

     return jigged_house_num     
     
def jigged_address(line_1: str):
     jigg_start = "".join(random.choice(string.ascii_uppercase) for i in range(4)) + " "
     jigg_end = line_1[-1]
     jigged_line_1 = ''.join((jigg_start,line_1,''))

     for _ in range(random_number(1,5)):
          jigged_line_1 = ''.join(("",jigged_line_1,jigg_end))     

     return jigged_line_1     

def jigged_line_2(line_2: str, house_number: str):
     a = ["house number ", "residence number ", "home number ", "number "]
     if line_2 == "":
          return random.choice(a) + jigged_house_num(house_number)
