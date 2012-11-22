#!/usr/bin/python
#sample python-mysql stuff
import mysql.connector as db
from checker import checkerFunction
#from mysql.connector import errorcode

class database(object):
  #build a connection string
  dbHost       = ''
  dbPort       = ''
  dbUsername   = ''
  dbPassword   = ''
  dbName       = ''
  _connection  = None
  _cursor      = None
  _instance    = None

  def __init__(self):
    try:
      if database._instance == None:
        self.dbHost      = 'dev.joubin.me'
        self.dbPort      = 3306
        self.dbUsername  = 'alex'
        self.dbPassword  = 'moya ucheba 123'
        self.dbName      = 'csc135'
        self._connect();
    except Exception, e:
      print "Errr: %s" % e

  def __del__(self):
    if self._cursor is not None:
      self._cursor.close()
    if self._connection is not None:
      self._connection.close()

  def _connect(self):
    try:
      self._connection = db.connect(user    = self.dbUsername,
                                   password = self.dbPassword,
                                   host     = self.dbHost,
                                   database = self.dbName)
      self._cursor = self._connection.cursor()
    except db.Error as e:
      print "Error: %s" % e

  """
  get all site hashes from db
  """
  def getSiteHashes(self):

    sitehashes   = dict()
    if self._connection is None:
      print "You must establish a connection first!"
      return

    try:
      commandText = ('''SELECT name, hash
                          FROM sites''')

      self._cursor.execute(commandText)
      for (name, sitehash) in self._cursor:
	sitehashes[name] = sitehash
      self._cursor.close()
      self._connection.close()

      for name in sitehashes:
	self._connect()
        print ("name: {} hash: {}".
          format(name, sitehashes[name]))

	newhash = checkerFunction(name)
        if sitehashes[name] == newhash:
          print "This site's privacy policy hash is up to date"
        else:
          sitehashes[name] = newhash
	  commandText = ("UPDATE sites SET hash='{}' WHERE name='{}';".format(sitehashes[name], name))
	  print commandText
	  self._cursor.execute(commandText)
	  self._connection.commit()
	  self._cursor.close()
	  self._connection.close()





    except db.Error as e:
      print "Error %s" % e





if __name__ == '__main__':
  dbInstance = database()
  dbInstance.getSiteHashes()
