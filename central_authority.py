from macpabe import *
from uit import UIT            # get uit attributes
from hospital import HOSPITAL  # get hospital attributes
import mysql.connector


db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  port='4306',
  database='CENTRAL_AUTHORITY'
)

class CENTRAL_AUTHORITY:
        def __init__(self, gid=None):
            # share parameter
            self.group = PairingGroup('SS512')
            self.maabe = MaabeRW15(self.group)
            self.public_parameters = self.maabe.setup()
            #self.secret_key_dict = None
            # user session
            self.gid = gid
        
        def user_is_exist(self, username):
            _cursor = db.cursor()
            query = ("SELECT USER_NAME FROM LOGIN "
                    "WHERE USER_NAME='%s'")
            _cursor.execute(query%(username))
            for (_user) in _cursor:
                print(_user)
                if (_user != None):
                    return True
            return False
        
        def register(self):
            print ("########### AUTHORITY REGISTER ###########")
            username = raw_input("user name: ")
            while (self.user_is_exist(username)):
                print ("User already exists. Try another username.")
                username = raw_input("user name: ")
            password = raw_input("password:  ")
            _cursor = db.cursor()
            if (True):
                if (True):
                    query = ("INSERT INTO LOGIN (USER_NAME, PASSWORD) "
                            "VALUES ('%s', '%s')")
                    _cursor.execute(query%(username, password))
                    db.commit()                   
                    author = "" # to save the user authorities
                    # create attribute list in hospital
                    choose = raw_input("Set attributes for HOSPITAL? [yes/no]")
                    while (choose == "yes" or choose == "no"):
                        if (choose == "yes"):
                            author  += "HOSPITAL"
                            Hospital = HOSPITAL()
                            Hospital.register(username)
                            break
                        elif (choose == "no"):
                            break
                        else:
                            choose = raw_input("Please type \"yes\" or \"no\":")

                    if (author != ""):
                        author += ", "

                    # create attribute list in uit
                    choose = raw_input("Set attributes for UIT? [yes/no]")
                    while (choose == "yes" or choose == "no"):
                        if (choose == "yes"):
                            author += "UIT"
                            Uit = UIT()
                            Uit.register(username)
                            break
                        elif (choose == "no"):
                            break
                        else:
                            choose = raw_input("Please type \"yes\" or \"no\"")
                    query = ("INSERT INTO AUTHORITIES (GID, AUTHORITIES) "
                            "VALUES ('%s', '%s')")
                    _cursor.execute(query%(username, author))
                    db.commit()
                    return True
            return False
        
        def login(self):
            print ("########### CENTRAL AUTHORITY ###########")
            username = raw_input("User name: ")
            password = raw_input("Password:  ")
            _cursor = db.cursor()
            query = ("SELECT USER_NAME, PASSWORD FROM LOGIN "
                    "WHERE USER_NAME='%s'")
            _cursor.execute(query%(username))
            for (user, pswd) in _cursor:
                #print ('pswd: '+pswd)
                if (password == pswd):
                    self.gid = username
                    return True
            return False


        def authority_list(self):
            _cursor = db.cursor()
            query = ("SELECT AUTHORITIES FROM AUTHORITIES " 
                    "WHERE GID = '" + self.gid + "'")
            _cursor.execute(query)
            x = None
            for (b) in _cursor:
                x = re.split(r', ', b[0])
            _cursor.close()
            return x
        
        def keyGenerator(self, secret_key_dict=None, attributes_list=None):
            if (self.login() and secret_key_dict != None and attributes_list != None):
                user_keys  = []
                _hospital  = []
                _uit       = []
                authorList = []
                for attr_auth in attributes_list:
                    (_, auth) = re.split(r'@',attr_auth)
                    if (auth == "HOSPITAL"):
                        _hospital.append(attr_auth)
                        if (auth not in authorList):
                            authorList.append(auth)
                    elif (auth == "UIT"):
                        _uit.append(attr_auth)
                        if (auth not in authorList):
                            authorList.append(auth)
                
                for author in authorList:
                        if (author == "HOSPITAL"):
                                #gid = self.gid
                                attributes = _hospital
                                user_key = self.maabe.multiple_attributes_keygen(self.public_parameters, 
                                                                                secret_key_dict["HOSPITAL"], 
                                                                                self.gid, 
                                                                                attributes)
                                user_keys.append(user_key)

                        elif (author == "UIT"):
                                attributes = _uit
                                user_key = self.maabe.multiple_attributes_keygen(self.public_parameters, 
                                                                                secret_key_dict["UIT"], 
                                                                                self.gid, 
                                                                                attributes)
                                user_keys.append(user_key)
                return {'GID': self.gid, 'keys': merge_dicts(user_keys)}
