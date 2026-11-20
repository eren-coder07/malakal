# Decompiled from Maradona.py
#
# Original was wrapped in 10 nested `exec(marshal.loads(...))` layers (CPython 3.9
# bytecode), and every string literal was hidden as
# `eval(marshal.loads(<code for bytes([...]).decode()>))`.
# All layers were peeled statically (nothing was executed) and the bytecode of
# the real payload was rebuilt by hand into the source below. Line numbers in
# comments match the original bytecode's line table.

copyright = '@psh_team'                                   # line 6

import os                                                 # line 7
try:                                                      # line 8
    import requests, json, random
    from urllib.parse import quote
    from base64 import b64encode, b64decode
    from binascii import unhexlify
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from datetime import datetime
    from time import sleep
except:                                                   # line 17
    os.system('pip install requests')
    os.system('pip install json')
    os.system('pip install wheel')
    os.system('pip install scipy')
    os.system('pip install pbkdf2')
    os.system('pip install pyaes')
    os.system('pip install pycryptodome')
    os.system('pip install pycrypto')
    os.system('pip install crypto')

# "Free trial" check: str(datetime.now()) -> 'YYYY-MM-DD ...', so dt is the month.
dt = str(datetime.now()).split('-')[1].split('-')[0]     # line 27
dt = int(dt)
if dt == 3 or dt > 3:                                     # line 29
    # NOTE: the original calls `exit(feval('[×] Free Trial END'))`; `feval` is never
    # defined, so in practice this raises NameError (the script still stops).
    exit('[×] Free Trial END')

us = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM'              # line 33
iv = b'lakQvjv3kB14B9lX'
password = b'Zj6gaCFzMmeTXuLuu3YFaRWIET7muIAs'


def enc(msg, iv, password):                               # line 36
    iv = iv
    password = password
    msg = pad(msg.encode(), AES.block_size)
    cipher = AES.new(password, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(msg)
    res = b64encode(cipher_text).decode('utf-8')
    return res


def dec(data):                                            # line 44
    iv = b'lakQvjv3kB14B9lX'
    password = b'Zj6gaCFzMmeTXuLuu3YFaRWIET7muIAs'
    data = pad(data.encode(), AES.block_size)
    decipher = AES.new(password, AES.MODE_CBC, iv)
    res = unpad(decipher.decrypt(b64decode(data)), AES.block_size).decode('utf-8')
    return res


u1 = '123456789'                                          # line 51 (unused)

h1 = {                                                    # line 52
    'Host': 'api.fowoii.com',
    'content-length': '2827',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Plume L2 Build/O00623; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://www.fowoii.com',
    'x-requested-with': 'com.space.mass.likes',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.fowoii.com/',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9,ar-DZ;q=0.8,ar;q=0.7',
}

dt1 = datetime.now()                                      # line 66
ts1 = str(datetime.timestamp(dt1)).split('.')[0]

head = {                                                  # line 68
    'Host': 'followlikes.store',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4IiwianRpIjoiYWQxMGU1MGU4NDE4MzAyNzU3YWM0ODBmNzRlOTQ3N2FiZjI4MGI5ZmNlMmQzNTM5YTliMjhkOTNiZjhkMzZkMDgwZjY5NzAzYjliODdjYzkiLCJpYXQiOjE2NjAwMzA2NDEsIm5iZiI6MTY2MDAzMDY0MSwiZXhwIjoxOTc1NjQ5ODQxLCJzdWIiOiIiLCJzY29wZXMiOlsiKiJdfQ.bwsLDroWJU_lF1jlR8TjxgO-gSGRG1jsD9jEjFrTh3zSWGYPpHbn1H-iU5citBsMaMTfR_eq03_Uq0UKGiEltrZIKhp6MM1dfyRyni2WGJVwTLFoIdyDfO7LMoi8UzmnYSiVHNRg8TA42xPXt0wJ1Twv2kthv1wMYArE9VP6uG2HEgDXuSSAFaKe5fJ5C7_gInxtpuhQ9wYXUl5xfaIFSIHG0YgA5OKBSXUQwss5FNx19c7zj7hbjyRlbIfjAElhdWfFeuet_cKVa0a8BvYqRrPzb4bhA2LQOzuVNu5GTZEz25H7ALTnnioT7LesYm2i1UQtqJVD0aitXT6Sk2b4xIa2i9tH2gQETrSc0zbZ5Ryc6EpBIW9QoFGOO_K8NsE8Xl_jN-BKa7nAcPThPTd11mKVKUqNP3pEP0uqoQ785vExmXfFeWGDE9wsDdeuINEN2YIQCZH2ak1o36nrrVQ8sQMUDMiXUu_H2eOIHH_qzOy8sMXDVSoIQXG_tCsxbW9UVm5acTKsE3arR80eeDStOCVXiGlTUneGaXMbM6Izv4jWzNQNcnZFNzVHDSDjYbS-cjKC1VwmvV1DkEIIntYjfY2TPYci6fWWcOvsZk6fP5pLpaE9rwPU_ZDC_-lOQ3si2aU1E2wzmBbUnbSnewQ-MGQn5mtvu-3l9hdFdc1LurY',
    'app-version': '9',
    'device-number': 'f95adeefae1e6199',
    'content-type': 'application/x-www-form-urlencoded',
    'content-length': '99',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/4.7.2',
}
dd = 'device_number=f95adeefae1e6199&client_secret=dQMe1kZhSjSyI23dZm7iftSiftMejTrfBkfgftem7q&client_id=8'  # line 77

E = '\033[1;31m'                                          # line 78
B = '\033[2;36m'
G = '\033[1;32m'
S = '\033[1;33m'

os.system('clear')                                        # line 82
print(f'{B}{E}=============================={B}\n|'
      f'{G}[+] GitHub    : {B}whisper-666 |\n|'
      f'{G}[+] InstaGram : {B}_whisper.io_|\n|'
      f'{G}[+] TeleGram  : {B}whisper_io  |\n'
      f'{E}==============================')
user = input(f'{G}[+] InstaGram UserName ==> {S}')  # line 88
print(f'{E}==============================')

# Step 1: resolve the Instagram username to a numeric id via followlikes.store
idr = requests.post(f'https://followlikes.store/api/users/{user}', data=dd, headers=head).json()  # line 90
pk = idr['fid']
pic = idr['avatar']
print(f'{G}[+] Your User ID ==> {S}{pk}')
print(f'{E}==============================')

# Step 2: log in to the fowoii "mass likes" app API with a random fake device id
ss = str(''.join(random.choice(us) for i in range(32)))  # line 95
msg = ('{"userId":"","productId":"com.fame.plus.follow","instUserId":"' + pk +
       '","version":"1.2.1","deviceInfo":{"deviceId":"' + ss +
       '","timezone":"+0100","timestamp":"' + ts1 +
       '","lang":"en","deviceModel":"PlumeL2","systemVersion":"8.0.0","regionCode":"US"},"loginId":"' + ss +
       '","otherLoginIds":["' + ss + '","' + pk + '"]}')
json = enc(msg, iv, password)                             # line 97
json = {'data': f'{json}'}
log = requests.post('https://api.fowoii.com/api/v1/user/login', json=json, headers=h1).json()['data']
data = log
login = str(dec(data))
uid = login.split('"userId":"')[1].split('"')[0]         # line 102

# Step 3: loop forever fetching "follow"/"like" tasks and reporting them as done
while True:                                               # line 103
    dt = datetime.now()
    ts = str(datetime.timestamp(dt)).split('.')[0]
    ss = str(''.join(random.choice(us) for i in range(32)))  # line 106
    msg = ('{"userId":"' + uid + '","productId":"com.fame.plus.follow","instUserId":"' + pk +
           '","version":"1.2.1","deviceInfo":{"deviceId":"' + ss +
           '","timezone":"+0100","timestamp":"' + ts +
           '","lang":"en","deviceModel":"PlumeL2","systemVersion":"8.0.0","regionCode":"US"},"types":["follow"]}')
    json = enc(msg, iv, password)                         # line 108
    json = {'data': f'{json}'}
    fo = requests.post('https://api.fowoii.com/api/v1/feed/get', json=json, headers=h1).json()['data']
    data = fo
    oid = dec(data)
    try:                                                  # line 113
        id = oid.split('"orderId":"')[1].split('"')[0]
        ort = oid.split('"orderType":"')[1].split('"')[0]
        if ort == 'follow':
            act = r'{\ "result\ ":\ "following\ ",\ "status\ ":\ "ok\ "}"}'
        if ort == 'like':
            act = r'{\ "status\ ":\ "ok\ "}"}'
    except:                                               # line 120
        if oid == '{"feeds":[],"limitDesc":"Oops! You click too fast. Relax your finger!","limitType":"requestTooFast","message":"Oops! You click too fast. Relax your finger! [undefined]","code":1}':
            pass
        else:
            pass
    try:                                                  # line 125
        ins = oid.split('"instUserId":"')[1].split('"')[0]
        msg = ('{"userId":"' + uid + '","productId":"com.fame.plus.follow","instUserId":"' + pk +
               '","version":"1.2.1","deviceInfo":{"deviceId":"' + ss +
               '","timezone":"+0100","timestamp":"' + ts +
               '","lang":"en","deviceModel":"PlumeL2","systemVersion":"8.0.0","regionCode":"US"},"feedId":"' + ins +
               '","feedType":"' + ort + '","orderId":"' + id + '","actResult":"' + act.replace(' ', ''))
        json = enc(msg, iv, password)                     # line 128
        json = {'data': json}
        cc = requests.post('https://api.fowoii.com/api/v1/feed/act', json=json, headers=h1).json()['data']
        data = cc
        r = dec(data)
        try:                                              # line 133
            coin = int(r.split('"balance":')[1].split(',')[0])
            print(f'{B}[+] Total Coins ==> {S}{coin}')
        except:
            if 'Repetitive Operation' in str(r):
                pass
            else:
                print(r)
    except:                                               # line 141
        pass
