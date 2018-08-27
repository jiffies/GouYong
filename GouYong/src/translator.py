#!/usr/bin/python3.5
#-*- coding:utf-8 -*-

from google import GoogleTranslate
from sogou import SogouTranslate
from youdao import YoudaoTranslate

class Translator(object):
    def __init__(self,  engine = 'google'):
        self.translators = []
        self.translators.append(GoogleTranslate())
        self.translators.append(SogouTranslate())
        self.translators.append(YoudaoTranslate())
        self.set_translator(engine)

    def set_translator(self, engine):
        for translator in self.translators:
            if engine == translator.engine:
                self.translator = translator

    def translate(self, text):
        result = self.translator.translate(text)
        if text == result:
            for translator in self.translators:
                result = translator.translate(text)
                if result != text:
                    break;
        return result

if __name__ == '__main__':
    translator = Translator()
    for who in ['google', 'sogou', 'youdao']:
        translator.set_translator(who)
        result = translator.translate("makes control reaches end of non-void functionv")
        print(result)
        result = translator.translate("apple")
        print(result)
        result = translator.translate("translate")
        print(result)
        result = translator.translate("GPIO_DIRECTION_OUTPUT")
        print(result)
