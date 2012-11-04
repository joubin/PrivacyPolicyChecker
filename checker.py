# The following code simply takes an input and downloads the privacy policy
# Usage: python checker.py amazon privacy policy
# will produce a file called amazon%20privacy%20policy
# if such file exists, it will create the above with a .tmp extention
# this code does not check

import _mysql
import urllib
#import urllib2
import sys
import requests
from readability.readability import Document
import os.path

# the commandline input
list = sys.argv 

#check array size
size = len(list)

# Google the input and use the first likes location
# This is the first result google gets 
google1 = 'http://www.google.com/search?hl=en&q='
google2 = '&btnI=1'
keyword = '%20'.join(list[1:size])

# Reconstruct the URL
url = google1 + keyword + google2
#Send URL Request 
r = requests.get(url, allow_redirects=False)
url = r.headers['location']

# Print URL for testing (Should be commented out during implementation as it will create noise)
print url

#Store the location of the file
fileExist =  os.path.isfile(keyword)

# Create a human readable document. Strips out most but NOT all of the html tags

html = urllib.urlopen(url).read()
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
