import _mysql
import urllib3
#import urllib32
import sys
import requests
from readability.readability import Document
import os.path


list = sys.argv
size = len(list)
google1 = 'http://www.google.com/search?hl=en&q='
google2 = '&btnI=1'
keyword = '%20'.join(list[1:size])

url = google1 + keyword + google2

r = requests.get(url, allow_redirects=False)
url = r.headers['location']
print url
fileExist =  os.path.isfile(keyword)

html = urllib3.urlopen(url).read()
readable_article = Document(html).summary()

if(fileExist):
	print "its there, ill make a temp"
	filename = keyword + ".tmp"
	f = open(filename, 'w')
	writeThis = str(readable_article)
	f.write(writeThis)
	f.close
else:
	print "no, its not there, ill go ahead and make it"
	filename = keyword
        f = open(filename, 'w')
        writeThis = str(readable_article)
        f.write(writeThis)
        f.close