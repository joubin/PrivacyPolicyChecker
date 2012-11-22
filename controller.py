import sys
import os
import threading
import pprint
from dbcalls import dbCalls
from threadedchecks import threadedCheck as check

maxThreads = 10

def main():
  threadLock = threading.Lock()
  threads = []
  db = dbCalls()
  for site in db.getSitesHashes():
    thread = check(threadLock, db, site['name'], site['name'], site['hash'])
    thread.start()
    threads.append(thread)
    #make sure we don't go over max concurrent thread limit
    while (threading.activeCount() > maxThreads):
      pass
  
  #wait for all threads to finish execution
  while (threading.activeCount() > 1):
    pass
  
  #display all users who need to be notified
  for user in db.getUsersToNotify():
    pprint.pprint(user)
  
if __name__ == '__main__':
  main()