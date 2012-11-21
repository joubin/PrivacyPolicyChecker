#sample python-mysql stuff
import mysql.connector as db
#from mysql.connector import errorcode

class baseDB(object):
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
        self.dbHost      = 'localhost'
        self.dbPort      = 3306
        self.dbUsername  = 'alex'
        self.dbPassword  = '""" password should go here"""'
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
  get all users
  """
  def getAllUsers(self):
    if self._connection is None:
      print "You must establish a connection first!"
      return
    
    try:
      commandText = ('''SELECT *
                          FROM users''')
      
      self._cursor.execute(commandText)
      for (userid, firstname, lastname, email) in self._cursor:
        print ("userid: {}, fname: {}, lastname: {}, email: {}".
          format(userid, firstname, lastname, email))
    
    except db.Error as e:
      print "Error %s" % e



if __name__ == '__main__':
  dbInstance = database()
  dbInstance.getAllUsers()

