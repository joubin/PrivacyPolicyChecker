from basesql import Basesql
import pprint

class dbCalls(Basesql):
  """
  get all users
  """
  def getAllUsers(self):
    if self._connection == None:
      print "You must establish a connection first!"
      return
    cursor = self._connection.cursor()
    result = []
    
    commandText = ('''SELECT *
                        FROM users''')
    try:  
      cursor.execute(commandText)
      columns = tuple( [d[0].decode('utf8') for d in cursor.description] )
      for row in cursor:
        result.append(dict(zip(columns, row)))
      cursor.close()
      return result
      
    except Exception as e:
      print "Error %s" % e
      return
  
  """
  add user
  """
  def addUser(self, fname, lname, email):
    if self._connection == None:
      print "You must establish a connection first!"
      return
    cursor = self._connection.cursor()
    
    commandText = ("""INSERT INTO users (firstname, lastname, email)
                           VALUES ("%s", "%s", "%s")"""%
                          (fname, lname, email))
    try:
      cursor.execute(commandText)
      #must commit updates/inserts/deletes
      self._connection.commit()
      commandText = ('''SELECT LAST_INSERT_ID()''')
      cursor.execute(commandText)
      result = cursor.fetchone()
      cursor.close()
      return result
      
    except Exception as e:
      print "Error %s" % e
      return

  """
  get site hash from db
  """
  def getSitesHashes(self):
    if self._connection == None:
      print "You must establish a connection first!"
      return
    cursor = self._connection.cursor()
    result = []
    
    commandText = ("""SELECT hash, name 
                        FROM sites """)
    try:
      cursor.execute(commandText)
      columns = tuple( [d[0].decode('utf8') for d in cursor.description] )
      for row in cursor:
        result.append(dict(zip(columns, row)))
      cursor.close()
      return result
      
    except Exception as e:
      print "Error %s" % e
      return
    

  """
  update site hash
  """
  def updateSiteHash(self, siteData):
    if self._connection == None:
      print "You must establish a connection first!"
      return
    
    cursor = self._connection.cursor()
    commandText = ("""UPDATE sites
                         SET isNew = 1,
                             hash  = '%s'
                       WHERE name  = '%s'""" %
                    (siteData['hash'], siteData['companyName']))
    try:
      cursor.execute(commandText)
      self._connection.commit()
      cursor.close()
    except Exception as e:
      print "%s" % e
    return
  
  """
  get users that need to be notified
  """
  def getUsersToNotify(self):
    if self._connection == None:
      print "You must establish a connection first!"
      return
    cursor = self._connection.cursor()
    result = []
    commandText = ("""SELECT u.firstname, u.lastname, u.email, x.companies
                        FROM (
                              SELECT uxs.userid, 
                                     group_concat(s.name ORDER BY s.name DESC SEPARATOR ', ') as companies
                                FROM usersxsites uxs
                              INNER JOIN sites s ON s.siteid = uxs.siteid
                               WHERE s.isnew = 1
                              GROUP BY uxs.userid
                            ) AS x
                      INNER JOIN users u ON u.userid = x.userid""")
    resetFlagCommand = ("""UPDATE sites SET isnew = 0 WHERE isnew = 1""")                
    try:
      cursor.execute(commandText)
      columns = tuple( [d[0].decode('utf8') for d in cursor.description] )
      for row in cursor:
        result.append(dict(zip(columns, row)))
      cursor.execute(resetFlagCommand)
      self._connection.commit()
      cursor.close()
      return result
      
    except Exception as e:
      print "%s" % e
      return
  
if __name__ == '__main__':
  dbInstance = dbCalls()
  stuff = dbInstance.getSitesHashes()
  pprint.pprint(stuff)
  """
  print("New userid: %s") % dbInstance.addUser('alex','c','alex@c')
  data = {"hash": 'blablabla', "companyName": 'amazon'}
  dbInstance.updateSiteHash(data)
  dataDict = dbInstance.getAllUsers()
  if (dataDict != None):
    #print ("userid\tfirstname\tlastname\temail")
    for row in dataDict:
      print ("{},  {},  {},  {}".
        format(row['userid'], row['firstname'], row['lastname'], row['email']))
  """  
  