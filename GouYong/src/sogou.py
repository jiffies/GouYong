#!/usr/bin/python3
import requests
import hashlib
import json
import random
from enum import Enum

class SogouLanguages(Enum):
    AR = 'ar'  # Arabic
    AUTO = 'auto'  # Arabic
    ET = 'et'  # Estonian
    BG = 'bg'  # Bulgarian
    PL = 'pl'  # Polish
    KO = 'ko'  # Korean
    BS_LATN = 'bs-Latn'  # Bosnian (Latin)
    FA = 'fa'  # Persian
    MWW = 'mww'  # Hmong Daw
    DA = 'da'  # Danish
    DE = 'de'  # German
    RU = 'ru'  # Russian
    FR = 'fr'  # French
    FI = 'fi'  # Finnish
    TLH_QAAK = 'tlh-Qaak'  # Klingon (pIqaD)
    TLH = 'tlh'  # Klingon
    HR = 'hr'  # Croatian
    OTQ = 'otq'  # Querétaro Otomi
    CA = 'ca'  # Catalan
    CS = 'cs'  # Czech
    RO = 'ro'  # Romanian
    LV = 'lv'  # Latvian
    HT = 'ht'  # Haitian Creole
    LT = 'lt'  # Lithuanian
    NL = 'nl'  # Dutch
    MS = 'ms'  # Malay
    MT = 'mt'  # Maltese
    PT = 'pt'  # Portuguese
    JA = 'ja'  # Japanese
    SL = 'sl'  # Slovenian
    TH = 'th'  # Thai
    TR = 'tr'  # Turkish
    SR_LATN = 'sr-Latn'  # Serbian (Latin)
    SR_CYRL = 'sr-Cyrl'  # Serbian (Cyrillic)
    SK = 'sk'  # Slovak
    SW = 'sw'  # Kiswahili
    AF = 'af'  # South African Common Dutch
    NO = 'no'  # Norwegian
    EN = 'en'  # English
    ES = 'es'  # Spanish
    UK = 'uk'  # Ukrainian
    UR = 'ur'  # Urdu
    EL = 'el'  # Greek
    HU = 'hu'  # Hungarian
    CY = 'cy'  # Welsh
    YUA = 'yua'  # Yucatec Maya
    HE = 'he'  # Hebrew
    ZH_CHS = 'zh-CHS'  # Chinese Simplified
    IT = 'it'  # Italian
    HI = 'hi'  # Hindi
    ID = 'id'  # Indonesian
    ZH_CHT = 'zh-CHT'  # Chinese Traditional
    VI = 'vi'  # Vietnamese
    SV = 'sv'  # Swedish
    YUE = 'yue'  # Cantonese
    FJ = 'fj'  # fijian
    FIL = 'fil'  # Filipino
    SM = 'sm'  # Samoan language
    TO = 'to'  # lea fakatonga
    TY = 'ty'  # Tahiti language
    MG = 'mg'  # Malagasy language
    BN = 'bn'  # Bengali

class SogouTranslate:

    SOGOU_API_URL = 'https://fanyi.sogou.com/reventondc/api/sogouTranslate'

    def __init__(self, pid: str='643622c12fd6fa85330057a8c350a9e5', secret_key: str='3979d815ce33296f768b636a05ae196a'):
        if (not pid) or (not secret_key):
            raise SogouTranslateException('pid or secret key cannot be empty')

        self.pid = pid
        self.secret_key = secret_key
        self.engine = 'sogou'

    def _generate_salt(self) -> str:
        return hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:19]

    def _compute_sign(self, source_text: str, salt: str) -> str:
        text = self.pid + source_text + salt + self.secret_key
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def _generate_data(self, source_text: str, from_language: SogouLanguages,
                       to_language: SogouLanguages):
        salt = self._generate_salt()
        data = {
            'q': source_text,  # text
            'from': from_language.value,  # from language
            'to': to_language.value,  # to language
            'pid': self.pid,  # pid
            'salt': salt,  # salt
            'sign': self._compute_sign(source_text, salt),  # sign
            'charset': 'utf-8',  # charset
            #     'callback': '', # optional for CORs
        }
        return data

    def translate(self, source_text: str, from_language: SogouLanguages = SogouLanguages.AUTO,
                  to_language: SogouLanguages=SogouLanguages.ZH_CHS) -> str:
        if not source_text:
            raise SogouTranslateException('Source text does not exist')

        data = self._generate_data(
            source_text, from_language, to_language
        )
        res = requests.post(self.SOGOU_API_URL, data=data)

        if not res.ok:
            raise SogouTranslateException(
                'Translation request is not successful'
            )

        json_res = json.loads(res.text)

        error_code = json_res['errorCode']
        if error_code != '0':
            return source_text

        return json_res['translation']

if __name__ == '__main__':
    text = 'makes control reaches end of non-void functionv'
    trans = SogouTranslate()
    zh_text = trans.translate(text)
    print(zh_text)
    text = 'GPIO_DIRECTION_OUTPUT'
    zh_text = trans.translate(text)
    print(zh_text)
