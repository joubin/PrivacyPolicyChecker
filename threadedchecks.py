import threading
import time
from array import *
#import database adapter
from dbcalls import dbCalls
from checker import checkerFunction

class threadedCheck(threading.Thread):
  """override constructor"""
  def __init__(self, threadLock, db, threadID, companyName, oldhash):
    self.threadID     = threadID
    self.db           = db
    self.threadLock   = threadLock
    self.companyName  = companyName
    self.oldhash      = oldhash
    threading.Thread.__init__(self)
    
    
  """override thread run function"""
  def run(self):
    #print ("starting threadid: %s") % self.threadID
    newhash = checkerFunction(self.companyName)
    #print("Thread: %s old hash: %s new hash: %s") % (self.threadID, self.oldhash, newhash)
    if (self.oldhash != newhash):
      data = {"hash": newhash, "companyName": self.companyName}
      self.threadLock.acquire()
      self.db.updateSiteHash(data)
      self.threadLock.release()
    

if __name__ == '__main__':
  threadLock = threading.Lock()
  threads = []
  db = dbCalls()
  for i in range(2):
    thread = threadedCheck(threadLock, db, i, "amazon", "oldhash")
    thread.start()
    threads.append(thread)