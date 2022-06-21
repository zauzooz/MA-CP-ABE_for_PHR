import mysql.connector
import re

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  port='4306',
  database='UIT'
)

class UIT:
  def __init__(self, central=None):
    self.central = central
    self.public_key = None
    self.secret_key = None
    if (self.central != None):
      (self.public_key, self.secret_key) = central.maabe.authsetup(central.public_parameters, 'UIT')
  
  def getPublicKey(self):
    return self.public_key

  def getSecretKey(self):
    return self.secret_key
  
  def register(self, gid):
    print ("UIT AUTHORITY ####################################")
    id       = raw_input("Id:            ")
    name     = raw_input("Name:          ")
    #gender   = raw_input("Gender:        ")
    #phone    = raw_input("Phone number:  ")
    role     = raw_input("Role:          ")
    #location = raw_input("Location:      ")
    year     = raw_input("Year of birth: ")

    _cursor  = db.cursor()
    query    = ("INSERT INTO UIT (GID, ID, NAME, ROLE, YEAR_OF_BIRTH) "
               "VALUES ('%s', '%s', '%s', '%s', '%s')")
    _cursor.execute(query%(gid, id, name, role, year))
    db.commit()

  def attributes_list(self, gid):
      _cursor = db.cursor()
      query = ("SELECT GID, ID, NAME,  ROLE, YEAR_OF_BIRTH FROM UIT " 
              "WHERE GID = '" + gid + "'")
      _cursor.execute(query)
      x = []
      for (_gid, id, name, role, year) in _cursor:
        x.append(id+"@UIT")
        x.append(name+"@UIT")
        x.append(role+"@UIT")
        x.append(year+"@UIT")
      _cursor.close()
      return x