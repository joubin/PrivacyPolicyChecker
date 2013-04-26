import datetime
import urllib
import hashlib
import sys
import requests
import os.path
import datetime
import os
from readability.readability import Document

"""
This is the base scanner that will compare page. 

This will work on html pages only. 

Some providers will provide their pages in PHP and that will not work. 

"""
def checkerFunction(myInput):
	today = datetime.date.today()
	try:
		google1 = 'http://www.google.com/search?hl=en&q='
		google2 = '%20privacy%20policy&btnI=1'
		keyword = myInput
		
		url = google1 + keyword + google2
		r = requests.get(url, allow_redirects=False)
		url = r.headers['location']
	except Exception as e:
		return


	
	myFullPath = "./sandbox/db/" + keyword

	if not os.path.exists("./sandbox"):
    	  os.makedirs("./sandbox")

	if not os.path.exists("./sandbox/db/"):
      	  os.makedirs("./sandbox/db/")

	if not os.path.exists(myFullPath):
    	  os.makedirs(myFullPath)

	filename = keyword + "." + str(today)
	filetowrite = myFullPath + "/" + filename
	
	fileExist =  os.path.isfile(filetowrite)
	
	
	
	
	if (url == None):
		return
	html = urllib.urlopen(url).read()
	readable_article = Document(html).summary()
	tempFileMade = False
	originalFileMade = False
	if(fileExist):
		filetowrite = filetowrite + ".tmp."
		f = open(filetowrite, 'w')
		writeThis = str(readable_article.encode('ascii', 'ignore')) 
		f.write(writeThis)
		f.close
		tempFileMade = True
	else:
		f = open(filetowrite, 'w')
		writeThis = str(readable_article.encode('ascii', 'ignore'))
		f.write(writeThis)
		f.close
		originalFileMade = True
	
	hashedmd5 = hashlib.md5(readable_article.encode('ascii', 'ignore'))
	hashedArticle = hashedmd5.hexdigest()
	return hashedArticle	
