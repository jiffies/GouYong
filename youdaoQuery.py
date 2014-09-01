import urllib2
import re
from string import Template
import os.path
import os
EXEPATH=os.path.split(os.path.realpath(__file__))[0]
os.chdir(EXEPATH)
CWD=os.getcwd()
TEMPLATEFILE=os.path.join(CWD,"youdao.temp")
QUERY = "http://dict.youdao.com/search?le=eng&q="
PATTERN=r'(?s)(<div id="results">.*)<div id="ads" class="ads">'
CACHEDIR="cache"
RESULTFILE="result.html"
def gettext(word):
    query = QUERY+word
    response = urllib2.urlopen(query).read()
    results=re.findall(PATTERN,response)
    return results[0]
    #return response
def creat_file(word,results):
    template=Template(file(TEMPLATEFILE).read())
    d={'results':results}
    s=template.substitute(d)   
    fileName=os.path.join(CACHEDIR,RESULTFILE)
    with file(fileName,'w') as f:
	    f.write(s)
    return fileName
if __name__=="__main__":
    pass
