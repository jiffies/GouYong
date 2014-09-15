#!-*- coding:utf-8 -*-
import logging


logging.basicConfig(level=logging.DEBUG,
        format='[%(levelname)s %(asctime)s %(module)s]:%(message)s')
def get_logger(name):
    return logging.getLogger(name)

