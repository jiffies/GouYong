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

if __name__=="__main__":
    setup(
        #setup_requires = [ "setuptools_git >= 0.3", ],
        name = "GouYong",
        version = '0.2',
        packages = find_packages(),
        #include_package_data=True,
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
        #exclude_package_data = {'': ['.gitignore']},
        author = "Jiffies",
        author_email = "lcqtdwj@gmail.com",
        description = "A translation software on  linux",
        license = "GPL",
        url = "https://github.com/jiffies/GouYong",
        classifiers=[
            'Natural Language :: Chinese (Simplified)',
            'Environment :: X11 Applications :: GTK',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 2.7',
        ],
    )
