from central_authority import *
from cloud import CLOUD
import os
from charm.core.math.pairing import hashPair as extractor
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction

central_user = CENTRAL_AUTHORITY()
cloud_user   = CLOUD()
uit          = UIT(central_user)
hospital     = HOSPITAL(central_user)
group = central_user.group
maabe = central_user.maabe
public_parameters = central_user.public_parameters
public_keys = {'HOSPITAL': hospital.public_key, 'UIT': uit.public_key}
secret_keys = {'HOSPITAL': hospital.secret_key, 'UIT': uit.secret_key}
attributes_list = None


def CA_get_attribute(central_user, i = 0):
    author_List = central_user.authority_list()
    attribute_list = []
    if (i == 0 ):
        for author in author_List:
            if (author == "HOSPITAL"):
                print ("############## HOSPITAL ##############")
                list = hospital.attributes_list(central_user.gid)
                for item in list:
                    print (item)
            elif (author == "UIT"):
                print ("############## UIT ##############")
                list = uit.attributes_list(central_user.gid)
                for item in list:
                    print (item)
        return
    else:
        for author in author_List:
            if (author == "HOSPITAL"):
                list = hospital.attributes_list(central_user.gid)
                for item in list:
                    attribute_list.append(item)
            elif (author == "UIT"):
                list = uit.attributes_list(central_user.gid)
                for item in list:
                    attribute_list.append(item)
            
        return attribute_list
    
def CA_working_screen():
    while (True):
        os.system("clear")
        print ("########### CENTRAL AUTHORITY ###########")
        print ("User: "+central_user.gid)
        print ("\t1. See your attributes.")
        print ("\t2. Get your attributes.")
        print ("\t3. Exit")
        option = raw_input("Type \"1\", \"2\" or \"3\": ")
        while(True):
            if (option == "1"):
                CA_get_attribute(central_user)
                # press anykey to exit
                press = raw_input("Press any key to exit.")
                break
            elif (option == "2"):
                global attributes_list
                attributes_list = CA_get_attribute(central_user=central_user, i = 1)
                print (attributes_list)
                press = raw_input("Press any key to exit.")
                break
            elif (option == "3"):
                central_user.gid = None
                return
            else:
                option = raw_input("Type \"1\", \"2\" or \"3\": ")

def CA_login_screen():
    #login = True
    while (True):
        os.system("clear")
        if(central_user.login()):
            # working space
            os.system("clear")
            CA_working_screen()
            return
        else:
            option = raw_input("Login faild. Do you want to login again? \"y\" or \"n\": ")
            while (True):
                if (option == "y"):
                    break
                elif (option == "n"):
                    return
                else:
                    option = raw_input("Type \"y\" or \"n\": ")

def CA_register_screen():
    while (True):
        central_user.register()
        os.system("clear")
        print ("Create accout successfull")
        press = raw_input("Press any key to exit.")
        return

def CA_first_screen():
    while (True):
        os.system("clear")
        print ("########### CENTRAL AUTHORITY ###########")
        print ("Type \"1\", \"2\" or \"3\": ")
        print ("\t1. Login")
        print ("\t2. Register")
        print ("\t3. Exit")
        option = raw_input ("Your option: ")
        while (True):
            if (option == "1"):
                os.system("clear")
                CA_login_screen()
                break
            if (option == "2"):
                os.system("clear")
                CA_register_screen()
                break
            if (option == "3"):
                os.system("clear") 
                return
            else:
                option = raw_input ("Your option: ")

def CLOUD_Download_File(cloud_user=cloud_user):
    print ("############### DOWNLOAD FILE ###############")
    global attributes_list
    cloud_user.listFile(attributes_list)
    print("\n")
    token = raw_input("Input token of file that you want to download: ")
    if (token in ["no","No","nO","NO"]):
        return
    (CT, en_key) = cloud_user.download(token)
    while (True):
        if (CT == "Token is Null."):
            token = raw_input("Token is Null.\nInput token of file that you want to download: ")
            if (token in ["no","No","nO","NO"]):
                return
            (CT, en_key) = cloud_user.download(token)
            pass
        elif (CT == "File does not exist."):
            token = raw_input("File does not exist.\nInput token of file that you want to download: ")
            if (token in ["no","No","nO","NO"]):
                return
            (CT, en_key) = cloud_user.download(token)
            pass
        else:
            break
    global secret_keys, attributes_list
    user_keys = central_user.keyGenerator(secret_key_dict=secret_keys, attributes_list=attributes_list)
    key = maabe.decrypt(public_parameters, user_keys, en_key)
    de = SymmetricCryptoAbstraction(extractor(key))
    data = de.decrypt(CT)
    print (data)
    # write output to a file
    press = raw_input("Press any key to exit.")
    return

def CLOUD_List_File(cloud_user=cloud_user):
    print ("############### YOUR UPLOADED FILE ###############")
    global attributes_list
    cloud_user.listFile(attributes_list)

def CLOUD_Upload_File(cloud_user=cloud_user):
    print ("############### UPLOAD FILE ###############")
    if (cloud_user.upload(group, maabe, public_parameters, public_keys)):
        print ("Upload successful.")
    wait = raw_input()

def CLOUD_Remove_File(cloud_user=cloud_user):
    if (cloud_user.remove_file()):
        print ("Remove successful.")
    else:
        print ("Don't remove anything.")
    wait = raw_input()

def CLOUD_working_screen():
    while (True):
        os.system("clear")
        print ("########### CLOUD ###########")
        print ("User: "+cloud_user.user)
        print ("Type 1, 2, 3 or 4: ")
        print ("\t1. See your file")
        print ("\t2. Download File") # (see file, get token, and then down load)
        print ("\t3. Upload File")
        print ("\t4. Remove File")
        print ("\t5. Logout")
        option = raw_input("Type \"1\", \"2\", \"3\", \"4\" or \"5\": ")
        while(True):
            if (option == "1"):
                os.system("clear")
                CLOUD_List_File(cloud_user)
                press = raw_input()
                break
            elif (option == "2"):
                os.system("clear")
                CLOUD_Download_File(cloud_user)
                # press any key to exit
                break
            elif (option == "3"):
                # press any key to exit
                os.system("clear")
                CLOUD_Upload_File(cloud_user)
                break
            elif (option == "4"):
                os.system("clear")
                CLOUD_Remove_File(cloud_user)
                break
            elif (option == "5"):
                cloud_user.logout()
                return
            else:
                option = raw_input("Type \"1\", \"2\", \"3\", \"4\" or \"5\": ")

def CLOUD_login_screen():
    #login = True
    while (True):
        os.system("clear")
        if(cloud_user.login()):
            # working space
            os.system("clear")
            CLOUD_working_screen()
            return
        else:
            option = raw_input("Login faild. Do you want to login again? \"y\" or \"n\": ")
            while (True):
                if (option == "y"):
                    break
                elif (option == "n"):
                    return
                else:
                    option = raw_input("Type \"y\" or \"n\": ")

def CLOUD_register_screen():
    while (True):
        cloud_user.register()
        os.system("clear")
        print ("Create accout successfull")
        press = raw_input("Press any key to exit.")
        return

def CLOUD_first_screen():
    while(True):
        os.system("clear")
        print ("########### CLOUD ###########")
        print ("Type \"1\", \"2\" or \"3\": ")
        print ("\t1. Login")
        print ("\t2. Register")
        print ("\t3. Exit")
        option = raw_input ("Your option: ")
        while (True):
            if (option == "1"):
                os.system("clear")
                CLOUD_login_screen()
                break
            if (option == "2"):
                os.system("clear")
                CLOUD_register_screen()
                break
            if (option == "3"):
                os.system("clear")
                global attributes_list
                attributes_list = None
                return
            else:
                option = raw_input ("Your option: ")

def main():
    while (True):
        os.system("clear")
        print ("Type \"1\", \"2\" or \"3\": ")
        print ("\t1. Central Authority")
        print ("\t2. Cloud")
        #print ("\t3. Exit")
        option = raw_input("Your option: ")
        while (True):
            if (option == "1"):
                os.system("clear")
                CA_first_screen()
            elif (option == "2"):
                os.system("clear")
                CLOUD_first_screen()
            #elif (option == "3"):
            #    os.system("clear")
            #    return
            else:
                option = raw_input("Type \"1\",\"2\" or \"3\": ")
            break

if __name__=="__main__":
    main()