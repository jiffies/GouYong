import urllib2
import re
from string import Template
TEMPLATEFILE="/home/lcq/python/exercise/youdao.temp"
def gettext(word):
    query = "http://dict.youdao.com/search?le=eng&q="+word
    response = urllib2.urlopen(query).read()
    results=re.findall(r'(?s)(<div id="results">.*)<div id="ads" class="ads">',response)
    return results[0]
    #return response
def creat_file(word,results):
	template=Template(file(TEMPLATEFILE).read())
	d={'results':results}
	s=template.substitute(d)
	fileName='cache/'+word
	f=file(fileName,'w')
	f.write(s)
	f.close()
	return fileName
if __name__=="__main__":
	pass
