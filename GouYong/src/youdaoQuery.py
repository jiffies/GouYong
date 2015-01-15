import urllib2
import urllib
import re
from string import Template
import os.path
import os
import log
logger = log.get_logger(__name__)
TIMEOUT = 5
EXEPATH=os.path.split(os.path.realpath(__file__))[0]
os.chdir(EXEPATH)
CWD=os.getcwd()
TEMPLATEFILE=os.path.join(CWD,"youdao.temp")
QUERY = "http://dict.youdao.com/search?le=eng&" #q="
PATTERN=r'(?s)(<div id="results">.*)<div id="ads" class="ads">'
CACHEDIR=os.path.join(os.path.expanduser('~'),".cache","GouYong")
try:
    os.mkdir(CACHEDIR)
except OSError:
    logger.info("cache folder exists.")
RESULTFILE="result.html"
def gettext(word):
    word = urllib.urlencode({'q':word})
    query = QUERY+word
    logger.info(query)
    response = urllib2.urlopen(query,timeout=TIMEOUT).read()
    results=re.findall(PATTERN,response)
    try:
        return results[0]
    except IndexError:
        logger.info("query fail")
        
    #return response
def creat_file(word,results,template=Template(file(TEMPLATEFILE).read()),
        fileName=os.path.join(CACHEDIR,RESULTFILE)):
    d={'results':results}
    s=template.substitute(d)   
    with file(fileName,'w') as f:
	    f.write(s)
    return fileName
if __name__=="__main__":
    pass
