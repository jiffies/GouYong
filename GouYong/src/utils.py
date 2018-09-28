#!-*- coding:utf-8 -*-
import time
from GouYong.src import log
logger = log.get_logger(__name__)

def tidy_text(text):
    return text.lower().strip()


def rgb_trans(r,g,b):
    return (r/255.,g/255.,b/255.)


class Timer(object):
    def __init__(self,verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self,*args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000
        if self.verbose:
            logger.debug("elapsed time: %f ms" % self.msecs)
