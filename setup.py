#!/usr/bin/env python
#-*- coding:utf-8 -*-
#from ez_setup import use_setuptools
#use_setuptools()
from setuptools import setup,find_packages
import os
import os.path
import sys
def get_data_files():
    data_files=[]
    for path,subdirs,files in os.walk("GouYong/share"):
        if files:
            data_files.append((os.path.join(sys.prefix,path[path.find('/')+1:]),[os.path.join(path,file) for file in files]))
    return data_files


setup(
    name = "GouYong",
    version = '0.1',
    install_requires = ['PyGObject','python-xlib'],
    packages = find_packages(),
    entry_points = {
        'gui_scripts':[
                'GouYong = GouYong.src.window:main'
            ]
        },

    package_data = {
        '':['*.temp'],
        #'GouYong':['cache/*','dict/*/*'],
        },
    data_files = get_data_files(),
    author = "Jiffies",
    author_email = "lcqtdwj@gmail.com",
    description = "A translator application run in Linux",
    license = "GPL",
    url = "https://github.com/jiffies/GouYong",
    classifiers=[
        'Natural Language :: Chinese (Simplified)',
        'Environment :: X11 Applications :: GTK',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
    ]
)
