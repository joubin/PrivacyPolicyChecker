# The following code simply takes an input and downloads the privacy policy
# Usage: python checker.py amazon privacy policy
# will produce a file called amazon%20privacy%20policy
# if such file exists, it will create the above with a .tmp extention
# this code does not check
import datetime
#import _mysql
import urllib
import md5
#import urllib2
import sys
import requests
from readability.readability import Document
import os.path
import datetime
import os
######################################################################################
######################################################################################
######################################################################################

today = datetime.date.today()
print today
# the commandline input
myInput = sys.argv[1] 


# Google the input and use the first likes location
# This is the first result google gets 
google1 = 'http://www.google.com/search?hl=en&q='
google2 = '%20privacy%20policy&btnI=1'
keyword = myInput

# Reconstruct the URL
url = google1 + keyword + google2
#Send URL Request 
r = requests.get(url, allow_redirects=False)
url = r.headers['location']

# Print URL for testing (Should be commented out during implementation as it will create noise)
print url

#Store the location of the file
myFullPath = "./sandbox/db/" + keyword
## ./sandbox/db/amazon/amazon.ddate
## ./sandbox/db/amazon/amazon.ddate.tmp


filename = keyword + "." + str(today)
filetowrite = myFullPath + "/" + filename

fileExist =  os.path.isfile(filetowrite)
print "filetowrite is %s" % filetowrite



#if not os.path.exists(myFullPath): os.makedirs(myFullPath)

# Create a human readable document. Strips out most but NOT all of the html tags

html = urllib.urlopen(url).read()
readable_article = Document(html).summary()
tempFileMade = False
originalFileMade = False
if(fileExist):
	print "its there, ill make a temp"
	filetowrite = filetowrite + ".tmp."
	f = open(filetowrite, 'w')
	writeThis = str(readable_article)
	f.write(writeThis)
	f.close
	tempFileMade = True
else:
	print "no, its not there, ill go ahead and make it"
	f = open(filetowrite, 'w')
	writeThis = str(readable_article)
	f.write(writeThis)
	f.close
	originalFileMade = True

