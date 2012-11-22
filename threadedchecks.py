import threading
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
    newhash = checkerFunction(self.companyName)
    if (self.oldhash != newhash):
      data = {"hash": newhash, "companyName": self.companyName}
      #db object is shared by other threads.
      #put a lock on this object until its done executing
      with self.threadLock:
        self.db.updateSiteHash(data)
        

if __name__ == '__main__':
  threadLock = threading.Lock()
  threads = []
  db = dbCalls()
  for i in range(2):
    thread = threadedCheck(threadLock, db, i, "amazon", "oldhash")
    thread.start()
    threads.append(thread)