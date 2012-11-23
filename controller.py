import sys
import os
import pprint
import threading
from Queue import Queue
from dbcalls import dbCalls
from checker import checkerFunction

"""
compare company old (db) hash to a new one (internet)
update sites if necessary
this class designed to be ran as a single daemon thread
"""
class threadedCheck(threading.Thread):
  """override constructor"""
  def __init__(self, threadLock, db, threadID, queue):
    self.threadID     = threadID
    self.db           = db
    self.threadLock   = threadLock
    self.queue        = queue
    threading.Thread.__init__(self)
    
  """override thread run function"""
  def run(self):
    while True:
      #try to get a job from queue
      site = self.queue.get()
      if (site != None):
        newhash = checkerFunction(site['name'])
        if (site['hash'] != newhash):
          data = {"hash": newhash, "companyName": site['name']}
          #db object is shared by other threads.
          #put a lock on this object until its done executing
          with self.threadLock:
            self.db.updateSiteHash(data)
        #notify queue that job is finished
        self.queue.task_done()

"""
check policies for all sites in the database
"""
def checkPolicies():
  queue = Queue()
  threadLock = threading.Lock()
  maxThreads = 15
  db = dbCalls()
  #spawn daemon threads that wait for jobs in queue
  for i in range(maxThreads):
    thread = threadedCheck(threadLock, db, i, queue)
    thread.setDaemon(True)
    thread.start()
  
  #put sites to process on queue
  for site in db.getSitesHashes():
    queue.put(site)
  
  #wait for all threads to finish execution
  queue.join()
  #display all users who need to be notified
  for user in db.getUsersToNotify():
    pprint.pprint(user)
  
if __name__ == '__main__':
  checkPolicies()