import mysql.connector
import re

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  port='4306',
  database='HOSPITAL'
)

class HOSPITAL:
  def __init__(self, central=None):
    self.central = central
    self.public_key = None
    self.secret_key = None
    if (self.central != None):
      (self.public_key, self.secret_key) = self.central.maabe.authsetup(self.central.public_parameters, 'HOSPITAL')

  def getPublicKey(self):
    return self.public_key

  def getSecretKey(self):
    return self.secret_key

  def register(self, gid):
    print ("HOSPITAL AUTHORITY ###########################")
    id       = raw_input("Id:            ")
    name     = raw_input("Name:          ")
    #gender   = raw_input("Gender:        ")
    #phone    = raw_input("Phone number:  ")
    #location = raw_input("Location:      ")
    year     = raw_input("Year of birth: ")
    role     = raw_input("Role:          ")

    _cursor  = db.cursor()
    query    = ("INSERT INTO HOSPITAL (GID, ID, NAME, ROLE, YEAR_OF_BIRTH ) "
            "VALUES ('%s', '%s', '%s', '%s', '%s')")
    _cursor.execute(query%(gid, id, name, role, year))
    db.commit()

  def attributes_list(self, gid):
    query = ("SELECT GID, ID, NAME, ROLE, YEAR_OF_BIRTH FROM HOSPITAL " 
            "WHERE GID = '" + gid + "'")
    _cursor = db.cursor()

    _cursor.execute(query)
    x = []
    for (_gid, id, name, role, year) in _cursor:
      x.append(id+"@HOSPITAL")
      x.append(name+"@HOSPITAL")
      #x.append(gender+"@HOSPITAL")
      #x.append(phone+"@HOSPITAL")
      #x.append(location+"@HOSPITAL")
      x.append(role+"@HOSPITAL")
      x.append(year+"@HOSPITAL")      
    _cursor.close()
    return x
