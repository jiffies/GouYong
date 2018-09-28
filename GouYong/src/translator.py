#!/usr/bin/python3.5
#-*- coding:utf-8 -*-

from GouYong.src.google import GoogleTranslate
from GouYong.src.sogou import SogouTranslate
from GouYong.src.youdao import YoudaoTranslate

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
        try:
            result = self.translator.translate(text)
            if text == result:
                for translator in self.translators:
                    result = translator.translate(text)
                    if result != text:
                        break;
            return result
        except:
            return text

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
