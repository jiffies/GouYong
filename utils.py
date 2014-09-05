#!-*- coding:utf-8 -*-

def tidy_text(text):
    return text.lower().strip()


def rgb_trans(r,g,b):
    return (r/255.,g/255.,b/255.)
