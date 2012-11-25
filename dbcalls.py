from basesql import Basesql
import pprint

"""
Database calls implementations
getAllUsers()               - returns all users
addUser(fname, lname, emai) - adds a user
getUsersToNotify()          - returns all users whos registered sites have been
                              resently updated (isnew flag set to 1).
                              Flag is reset after retrieval
getUserSites(userEmail)     - returns all sites registered for a single user
getSitesHashes()            - returns name of the sites and their hashes
setSiteToUser(companyName, email) - assign site to a single user                         
addSite()                   - add a site to the daatabase
getAllSite()                - returns a list of all sites
"""

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

  """
  get all companies for a given user
  """
  def getUserSites(self, userEmail):
    if self._connection == None:
      print "You must establish a connection first!"
      return
    cursor = self._connection.cursor()
    result = []
    
    commandText = ("""SELECT s.name
                        FROM sites s
                      INNER JOIN usersxsites uxs ON uxs.siteid = s.siteid
                      INNER JOIN users u ON u.userid = uxs.userid
                      WHERE u.email = '%s'""" % userEmail)
             
    try:
      cursor.execute(commandText)
      columns = tuple( [d[0].decode('utf8') for d in cursor.description] )
      for row in cursor:
        result.append(dict(zip(columns, row)))
      cursor.close()
      return result

    except Exception as e:
      print "%s" % e
      return
  
  """
  assigns a site to a single user 
  """
  def setSiteToUser(self, companyName, email):
    if self._connection == None:
      print "You must establish a connection first!"
      return
    cursor = self._connection.cursor()
    result = None
    commandText = ("""INSERT INTO usersxsites (userid, siteid)
                        SELECT u.userid, s.siteid
                          FROM users u, sites s
                         WHERE u.email = '%s'
                           AND s.name = '%s'"""%
                           (email, companyName))
    try:
      cursor.execute(commandText)
      if (cursor.rowcount == 1):
        self._connection.commit()
        cursor.close()
        return
      else:
        self._connection.rollback()
        cursor.close()
        return "User email or company name supplied don't exist"
    except Exception as e:
      return "Error adding records %s" % e
     
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
  add site
  """
  def addSite(self, sitename):
    if self._connection == None:
      print "You must establish a connection first!"
      return
    cursor = self._connection.cursor()
    
    commandText = ("""INSERT INTO sites (name)
                           VALUES ("%s")"""%
                          (sitename))
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
  get all users
  """
  def getAllSites(self):
    if self._connection == None:
      print "You must establish a connection first!"
      return
    cursor = self._connection.cursor()
    result = []
    
    commandText = ('''SELECT name
                        FROM sites''')
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
 
  
if __name__ == '__main__':
  dbInstance = dbCalls()
  """
  pprint.pprint(dbInstance.setSiteToUser('facebook','alex@test'))
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
  
