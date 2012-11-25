#!/usr/bin/python

from dbcalls import dbCalls
from controller import *

class UserInterface(object):

  """
	Option 1 	Adds a user to the database
	Option 2	Adds a userxsite to the database and adds a site if it doesn't exist already
	Option 3	Runs the controller
  """

  def showMenu():

    db = dbCalls()
    exitFlag = 0

    print "=================================="
    print "=      Privacy Policy Checker    ="
    print "=================================="
    print "= 1) Add User                    ="
    print "= 2) Register for Updates        ="
    print "= 3) Run Controller              ="
    print "=                                ="
    print "= 9) Exit                        ="
    print "=================================="
    userInput = raw_input("Please select an option: ")

    if userInput == '1':
      firstname = raw_input("First Name: ")
      lastname = raw_input("Last Name: ")
      email = raw_input("E-mail Address: ")
      db.addUser(firstname, lastname, email)
    elif userInput == '2':
      existingFlag = 0
      email = raw_input("E-mail: ")
      sitename = raw_input("Company Name: ")
      existingSites = db.getAllSites()

      for name in existingSites:
	for key in name:
          if name[key] == sitename:
	    existingFlag = 1
	
      if existingFlag == 0:
	db.addSite(sitename)

      db.setSiteToUser(sitename, email)
    elif userInput == '3':
     print "Updating Privacy Policy hashes..."
     checkPolicies()
    elif userInput == '9':
      exitFlag = 1
    else:
      print "Input not recognized. Please choose an option from the menu"

    print ""

    return exitFlag

  if __name__ == '__main__':
    while(showMenu() == 0):
      pass
    print "Goodbye!"
