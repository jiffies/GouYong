#!/usr/bin/python3.5
#-*- coding:utf-8 -*-

import re
import requests
from GouYong.src.translator import Translator

class Cht(object):
    def __init__(self, url = "https://cht.sh/"):
        self.url = url

    def query(self, text):
        data = re.sub(r' ', '/', text.lstrip().rstrip(), 1)
        data = self.url + data.replace(' ', '+') + '?T'
        r = requests.get(data)
        return r.text

if __name__ == '__main__':
    translator = Translator()
    text = 'makes control reaches end of non-void functionv'
    cht = Cht()
    note = cht.query(text)
    c = translator.translate(note)
    print(c)
