from macpabe import *
from central_authority import CENTRAL_AUTHORITY
from hospital import HOSPITAL
from uit import UIT
from cloud import CLOUD
import mysql.connector
from charm.core.math.pairing import hashPair as extractor
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
        

if __name__=="__main__":
        print("Start!!!")
        central  = CENTRAL_AUTHORITY()
        hospital = HOSPITAL(central)
        uit      = UIT(central)
        public_keys = {'HOSPITAL': hospital.public_key, 'UIT': uit.public_key}
        secret_keys = {'HOSPITAL': hospital.secret_key, 'UIT': uit.secret_key}

        key = central.group.random(GT)
        # serialize key
        access_policy = '(H3357@HOSPITAL and 20521858@UIT) or DR007@HOSPITAL'
        msg = CLOUD().convertToBinaryData("/home/nnt/MA-CP-ABE/PHR/phr2.txt")
        if (central.login()):                
                user_keys = central.keyGenerator(secret_key_dict=secret_keys)
                        # Create a random key              
                en = SymmetricCryptoAbstraction(extractor(key))
                ct = en.encrypt(msg)
                print (ct)
                        #Encrypt the key               
                cipher_key = central.maabe.encrypt(central.public_parameters, public_keys, key, access_policy)
                print (cipher_key)
                print(len(cipher_key))
                        #Decrypt the key
                decrypted_key = central.maabe.decrypt(central.public_parameters, user_keys, cipher_key)
                de = SymmetricCryptoAbstraction(extractor(decrypted_key))
                print(de.decrypt(ct))
        else:
                print("Username or Password is incorrect!!!")