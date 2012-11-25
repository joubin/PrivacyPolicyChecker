#sample python-mysql stuff
import mysql.connector as db
#from mysql.connector import errorcode
from ConfigParser import SafeConfigParser

class Basesql(object):
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
    if self._instance == None:
      parser = SafeConfigParser()
      parser.read('config.ini')
      self.dbHost      = parser.get('dbConnectionString', 'dbHost')
      self.dbPort      = parser.get('dbConnectionString', 'dbPort')
      self.dbUsername  = parser.get('dbConnectionString', 'dbUsername')
      self.dbPassword  = parser.get('dbConnectionString', 'dbPassword')
      self.dbName      = parser.get('dbConnectionString', 'dbName')
      try:
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
    except db.Error as e:
      print "Error: %s" % e
  
  

