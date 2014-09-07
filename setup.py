#!/usr/bin/env python
#-*- coding:utf-8 -*-
from setuptools import setup,find_packages

setup(
    name = "GouYong",
    version = '0.1',

    install_requires = ['PyGObject','python-xlib'],
    #package_dir = {
        #'dict':'dict',
        #'cache':'cache',
        #},
        ##'':'src',
        ##'':'lib',},
    packages = find_packages(),
    #include_package_data=True,
    entry_points = {
        'gui_scripts':[
                'GouYong = GouYong.src.window:main'
            ]
        },

    #data_files = [
            #('dict',['dict/*']),
            #('cache',['cache/*']),
        #],
    package_data = {
        '':['*.png','*.temp','*.desktop'],
        'GouYong':['cache/*','dict/*/*'],
        },
    data_files = [
            ('/usr/share/applications/',['GouYong/src/GouYong.desktop']),
            ('/usr/share/GouYong/',['GouYong/icon.png']),
        ],
    author = "Jiffies",
    author_email = "lcqtdwj@gmail.com",
    description = "A dict application run in Linux",
    license = "GPL",
    url = "https://github.com/jiffies/GouYong",
        )
