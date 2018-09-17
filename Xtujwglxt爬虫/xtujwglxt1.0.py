from bs4 import BeautifulSoup
from PIL import Image
import requests
import json
import re

class Login(object):
    def __init__(self):
        self.headers = {
            'Host' : 'jwxt.xtu.edu.cn',
            'Referer' : 'http://jwxt.xtu.edu.cn',
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
        }
        self.login_url = 'http://jwxt.xtu.edu.cn/jsxsd'
        self.post1_url = 'http://jwxt.xtu.edu.cn/jsxsd/xk/LoginToXk'
        self.post2_url = 'http://jwxt.xtu.edu.cn/jsxsd/xk/LoginToXk?flag=sess'
        self.logined_url = 'http://jwxt.xtu.edu.cn/jsxsd/kscj/cjcx_list?xq=2017-2018-2'
        self.session = requests.Session()

    def getCode(self):
        response = self.session.get(self.login_url, headers=self.headers)
        r = self.session.get(self.login_url+'/verifycode.servlet')
        with open('1.jpg','wb') as f:
            for chk in r:
                f.write(chk)
            f.close()
        code = input("验证码：")
        return (code)

    def getEncoded(self,username, password):
        r = self.session.get(self.login_url, headers=self.headers)
        response = self.session.post(self.post2_url, headers=self.headers)
        data = response.json().get('data')
        encoded = ""
        scode = data.split("#")[0]
        sxh = data.split("#")[1]
        code = username + "%%%" + password

        for i in range(0, len(code)):
            if (i < 20):
                encoded = encoded + code[i:i + 1] + scode[0:int(sxh[i:i + 1])]
                scode = scode[int(sxh[i:i + 1]):len(scode)]
            else:
                encoded = encoded + code[i:len(code)]
                break

        return encoded

    def login(self,username,password):
        post_data = {
            'USERNAME' : username,
            'PASSWORD' : password,
            'encoded' : self.getEncoded(username=username, password=password),
            'RANDOMCODE': self.getCode()
        }

        response = self.session.post(self.post1_url, data=post_data,headers=self.headers)
        r = self.session.get(self.logined_url, headers=self.headers)
        self.profile(html=r)


    def profile(self,html):
        html.encoding = 'utf-8'
        text = html.text
        soup = BeautifulSoup(text,'lxml')
        for tr in soup.find_all(name ='tr'):
            for td1 in tr.find_all(attrs = {'align':'left'}):
                print(td1.string,end='')
            for td2 in tr.find_all(name = 'a'):
                print("  "+td2.string)


if __name__ =="__main__":
    username = input("学号:")
    password = input("密码:")
    login = Login()
    login.login(username=username, password=password)





