#!/usr/bin/python3.5
#-*- coding:utf-8 -*-

from googletrans import Translator

class GoogleTranslate(object):
    def __init__(self, url = 'translate.google.cn'):
        self.translator = Translator(service_urls=[url])
        self.engine = 'google'

    def translate(self, text):
        result = self.translator.translate(text,dest="zh-CN")
        return result.text

if __name__ == '__main__':
    text = 'makes control reaches end of non-void functionv'
    y = GoogleTranslate()
    result = y.translate(text)
    print(result)
    result = y.translate("apple")
    print(result)
    result = y.translate("translate")
    print(result)
