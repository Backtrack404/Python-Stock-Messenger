from cgi import print_form
import socket
import ssl
import json
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256 as SHA
from cryptography.fernet import Fernet
from Decrypt import RSADecrypt, ParsJson
from dbconn import DataBase
from getS3 import S3
HOST = '3.34.122.130'
PORT = 8007

context = ssl._create_unverified_context()
context.load_verify_locations('D:\\Code\\Project\\SSL_Socket\\PythonSSL\\client.crt')

data = ''
count = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as rcv_data:
        rcv_data.connect((HOST,PORT))
        
        while True:
            if(rcv_data != " "):
                JsonData = json.loads(rcv_data.recv(4096).decode("utf-8"))
                
                print(f"count: {count}")
                #print(data)
                count += 1
                # print(JsonData+"\n")
                # JsonData = Decrypt(str(JsonData)).decode("utf-8")
                # print(JsonData)
                
                encKey = JsonData['encKey']
                data = JsonData['data'] 
                pinId = JsonData['pinId']
                type = JsonData['type']  
                
                print(data)  
                print()
                print(pinId)
                print()
                print(type) 
                print()
                print(encKey)
                print()
                
                AES = RSADecrypt(encKey, data)
                filePath = ParsJson(AES)
                
                certi_company, certi_name = DataBase.getUseDocData(pinId)
                S3.getS3(certi_name)
                S3.unzip(certi_company, certi_name)
                
                
                

                
                
        # decryptor = PKCS1_OAEP.new(privateKey.encode('ascii'))
        # decMessage = decryptor.decrypt(data)
        # print(decMessage)
        
    
        #data = json.loads(s.recv(1024).decode('utf-8'))
               
        #var_auth = data[0] 
        #var_input = data[1]
        #var_output = data[2]