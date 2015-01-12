#!/usr/bin/env python
#!-*- coding:utf-8 -*-
import optparse
import os
MAINTAINER = "Jiffies<lcqtdwj@gmail.com>"
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
    cmd = r"fpm -s python -t deb -m '%s' -n %s %s setup.py"
    os.system(cmd % (MAINTAINER,NAME,generate_dependency()))

def clean():
    os.system("rm -R dist deb_dist tmp GouYong.* GouYong-*")

def stdeb4ppa():
    os.system("python setup.py --command-packages=stdeb.command sdist_dsc")

def main():
    p = optparse.OptionParser(description="build GouYong for launchpad.",
            usage="""
            python build_dist.py --lp
            python build_dist.py --clean
            """)
    p.add_option('--lp',action="store_true",help="build and upload to launchpad.")
    p.add_option('--clean',action="store_true",help="remove tmp file.")
    
    options,arguments=p.parse_args()
    if options.lp:
        stdeb4ppa()
    elif options.clean:
        clean()


if __name__=="__main__":
    main()
