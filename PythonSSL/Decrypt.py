from ast import Bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Cryptodome.Cipher import AES
from base64 import b64decode
from Cryptodome.Util.Padding import pad, unpad
from binascii import unhexlify
import json

encKey = """dU277LijeaLUF7vtkzXz9x7iy85hQO8BcZWZP3nT/QPg1tQGDlq200t3dZjfn6OibPsIibngxEMT
tX+i1BNuWMO0HLDjulhJ+6vdNrwBW2lg/LO1YvqZWRE4M8uyuJ+7NeQX6nJMOzm16IDLAq/swcvO
7qL+zxdY6WxEfPAVuHUpfpCjJ4Wb3kR/7+pzKYDR4JvRatTBsV5Q24BXIfB5GcgEG5NPUvJJ/mRP
8Iav08wSiYTnxDFH2HTno7MxsTsGAB78nCZUm27U7dhGbiy5XP+DjbL4iYeGpLL7Drhe4c0OBuDn
D+z7EnIZKsYCtBgjlRopXdnjABVh9D7abkQGMojmmMmYvJ7LzEKwBPKQsc1OCkAChAlYgz6GEJ3e
rE0xuIhCsKYRoWeKbW+2El6GcpzTQCiQBM+K1kQVxr5EOAc6DMz+wvl4q+dN0wE7YvaoVCfPcono
iGsfNIyYjfSNuyk12CFq7Ozt6l3rKvkV89CiMoGw5V7wa1G5476qwVXxjDotikUR1JhfWH/6AMJc
DH39gR4BVq40so0/yB8F8gT8T3rB+GNrBvFAD/6OmIgWpvu2hWucnowB1ZO2aklaOS2HnhLrbPAP
FKr0kSQI+MJTxps80GGwkmHzVn64HSpdiCLP8kzbYMWVRBdRiC1cHThhwlDwCGzRqJ2pgnqxSX4="""

data = """4yf3unPAfJycs/kcpvi7GUcYGoW3s9xY8nQ/xGmO8UyXm4LmQhqja5vfoiCiVWhWt+cj3zzYHSPXRhuppwz21CthFl1QzQ6zIB3/VXLzoyB1QTS+SCNg5Ti2QQfZZICpeBmor6V5lTkIeWSvaXv7B7dY4539pKYUKGpgpVUWSsdNyNcWC/dhyy/zu0YGLis5F0HDPGg5NRB/RcHEjvQjgj9KCxM2j6VJyOcThZlG8DgAc+bsiQ2Oa3cX1cTcYbVrnq6IDIQR6WDQUz+7/Ge3mpki9SkISoZyPI/iullDXKgecoIxpOwQvD/gfUrwKvMBLN8th63JwMDFOrdTBshatw=="""

def RSADecrypt(RSAEncrypted, AESEncrypted):
    fPri = open('/Users/strelka/Programming/회사/Project/Code/Project/SSL_Socket/PythonSSL/private.pem', 'rb')
    prikey = RSA.importKey(fPri.read())
    fPri.close()
    raw_cipher_data = b64decode(RSAEncrypted)
    cipher = Cipher_PKCS1_v1_5.new(prikey)
    phn = cipher.decrypt(raw_cipher_data, None)

    JsonData = json.loads(phn)
    key = JsonData['key'].encode('utf-8')
    iv = JsonData['iv'].encode('utf-8')
    
    # print(f"key: {key}")
    # print(f"iv: {iv}")
    
    enc = b64decode(AESEncrypted)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    DecJson = cipher.decrypt(enc).decode("utf-8", "ignore").strip()
    
    print(DecJson)
    
    return DecJson



def ParsJson(DecJson):
    JsonData = json.loads(DecJson)
    
    postData = JsonData['postData']

    person_name = postData['person_name']
    jumin_first = postData['jumin_first']
    jumin_second = postData['jumin_second']
    certi_name = postData['certi_name']
    certi_password = postData['certi_password']
    person_address1 = postData['person_address1']
    person_address2 = postData['person_address2']
    certi_company = postData['certi_company']

    print(f'person_name: {person_name}')
    print(f'jumin_first {jumin_first}')
    print(f'jumin_second {jumin_second}')
    print(f'certi_name {certi_name}')
    print(f'certi_password {certi_password}')
    print(f'person_address1 {person_address1}')
    print(f'person_address2 {person_address2}')
    print(f'certi_company {certi_company}')
    
    return certi_company, certi_name
    
    
        

AES = RSADecrypt(encKey, data)
ParsJson(AES)

