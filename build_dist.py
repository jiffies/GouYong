#!/usr/bin/env python
#!-*- coding:utf-8 -*-
import os

NAME = "GouYong"
DEP = "DEPENDENCY"
FPM_D = r"-d '%s'"

def generate_dependency():
    items = []
    with file(DEP) as f:
        for line in f:
            items.append(FPM_D % line.rstrip('\n'))
    return  ' '.join(items)

def build_deb():
    cmd = r"fpm -s python -t deb -n %s %s setup.py"
    os.system(cmd % (NAME,generate_dependency()))

def clean():
    pass



def main():
    build_deb()

if __name__=="__main__":
    main()
