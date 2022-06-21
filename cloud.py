from macpabe import *
from uit import UIT
from hospital import HOSPITAL
from central_authority import *
import mysql.connector
from charm.core.math.pairing import hashPair as extractor
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
import random
import string


db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  port='4306',
  database='CLOUD'
)

class CLOUD:
    def __init__(self):
        self.user = None
        self.section_key = None

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
        username     = raw_input("User name:     ")
        while (self.user_is_exist(username)):
            print ("User already exists. Try another username.")
            username = raw_input("user name:     ")
        password     = raw_input("Password:      ")
        phone_number = raw_input("Phone number:  ")
        email        = raw_input("Email:         ")
        year         = raw_input("Year of birth: ")
        _cursor = db.cursor()
        query = ("INSERT INTO LOGIN (USER_NAME, PASSWORD, PHONE_NUMBER, EMAIL, YEAR_OF_BIRTH) "
                "VALUES ('%s', '%s', '%s', '%s', '%s')")
        _cursor.execute(query%(username, password, phone_number, email, year))
        db.commit()

    def login(self):
        print ("########### LOGIN CLOUD ###########")
        username = raw_input("User name: ")
        password = raw_input("Password:  ")
        _cursor = db.cursor()
        query = ("SELECT USER_NAME, PASSWORD FROM LOGIN "
                "WHERE USER_NAME='%s'")
        _cursor.execute(query%(username))
        for (user, pswd) in _cursor:
            if (pswd == password):
                self.user = user
                return True
        return False

    def is_user_accessed(self, token, user_attribute):
        if (self.user != None):
            pass
        else:
            return

    # list file khi co attribute thoa
    def listFile(self, user_attribute=None):
        file_list = []
        if (self.user != None):
            _cursor = db.cursor()
            _query = ("SELECT USER_NAME, TOKEN, FILE_NAME, POLICY FROM FILE_UPLOAD "
                    "WHERE USER_NAME='%s'")
            _cursor.execute(_query%(self.user))
            for (_user, token, fileName, policy) in _cursor:
                file_list.append(token + ": " + fileName)
            if (user_attribute != None):
                query = ("SELECT USER_NAME, TOKEN, FILE_NAME, POLICY FROM FILE_UPLOAD ")
                _cursor.execute(query)
                check = False
                for (_user, token, fileName, policy) in _cursor:
                    if (token + ": " + fileName not in file_list):
                        check = False
                        _policy = eval(policy)
                        for _list in _policy:
                            i = 0
                            for attr in user_attribute:
                                if (attr in _list):
                                    i = i + 1
                            if (i == len(_list)):
                                check = True
                                break
                            else:
                                check = False
                        if (check):
                            file_list.append(token + ": " + fileName)
            stt = 1
            for item in file_list:
                print (str(stt)+ ": " + item)
                stt = stt + 1

    def createPolicy(self):
        if (self.user != None):
            print ("Type \"no\" to end add the policy")
            policy = []
            _policy = ""
            _str = ""
            while (True):
                _str = raw_input("Add attribute who can access: ")
                if (_str not in ['no', 'No', 'nO', 'NO']):
                    if (_policy != ""):
                        _policy = _policy + " or "
                    _policy = _policy + "(" +_str + ")"
                    attributes = re.split(r' and ', _str)
                    y = []
                    for attr in attributes:
                        y.append(attr)
                    policy.append(y)
                else:
                    break
            return (_policy, str(policy))

    def convertToBinaryData(self, filepath):
        with open(filepath, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def token_is_exists(self, token):
        _cursor = db.cursor()
        query = ("SELECT TOKEN FROM FILE_UPLOAD "
                "WHERE TOKEN='%s'")
        _cursor.execute(query%(token))
        for (_token) in _cursor:
            if (_token != None):
                return True
        return False

    def upload(self, group, maabe, public_parameters, public_keys):
        if (self.user != None):
            filepath = raw_input("Choose your file: ")    
            letters  = string.hexdigits
            # token is unique
            token = ''.join(random.choice(letters) for i in range(50))
            fileName = re.split(r'\/', filepath)[-1]
            while (self.token_is_exists(token)):
                token = ''.join(random.choice(letters) for i in range(50))
            key = group.random(GT)
            upload_data = self.convertToBinaryData(filepath)
            (policy, _policy)   = self.createPolicy()
            # encrypt upload_data
            en = SymmetricCryptoAbstraction(extractor(key))
            upload_data = en.encrypt(upload_data)
            en_key = maabe.encrypt(public_parameters, public_keys, key, policy)
            # enctypt key

            _cursor = db.cursor()
            query = ("INSERT INTO FILE_UPLOAD (USER_NAME, TOKEN, FILE_NAME, DATA, ENCRYPT_KEY, POLICY) "
                    "VALUES ('%s', '%s', '%s', '%s', \"%s\", \"%s\")")
            print (query%(self.user, token, fileName, upload_data, en_key, _policy))
            _cursor.execute(query%(self.user, token, fileName, upload_data, en_key, _policy))
            db.commit()
            return True

    def download(self, token=None):
        if (self.user != None):
            if (token == None):
                return ("Token is Null.", 0)
            else:
                if (self.token_is_exists(token)):
                    _cursor = db.cursor()
                    query = ("SELECT TOKEN, DATA, ENCRYPT_KEY FROM FILE_UPLOAD "
                            "WHERE TOKEN='%s'")
                    _cursor.execute(query%(token))
                    for (_token, _data, _en_key) in _cursor:
                        return (_data, _en_key)
                else:
                    return ("File does not exist.",0)

    def remove_file(self):
        if (self.user != None):
            self.listFile()
            print("\n")
            token = raw_input("Input token of a file you want to delete: ")
            while (True):
                if (self.token_is_exists(token)):
                    break
                elif (token in ['no','No','nO','NO']):
                    return None
                else:
                    token = raw_input("Input token of a file you want to delete: ")
            _cursor = db.cursor()
            choose = raw_input("Do you want to delete the file (\"y\" or \"n\"): ")
            while (True):
                if (choose == "y"):
                    query = ("DELETE FROM FILE_UPLOAD "
                            "WHERE TOKEN='%s'")
                    _cursor.execute(query%(token))
                    db.commit()
                    return True
                elif (choose == "n"):
                    return None
                else :
                    choose = raw_input("Please type \"y\" or \"n\": ")

    def logout(self):
        self.user = None