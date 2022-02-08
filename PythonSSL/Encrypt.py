from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import binascii

fPri = open('private.pem', 'rb')
fPub = open('public.pem', 'rb')

 

prikey = RSA.importKey(fPri.read())
pubKey = RSA.importKey(fPub.read())


#RSA Encryption Using Public Key
fp = open('file.txt', 'rb')

cipherKey = Cipher_PKCS1_v1_5.new(pubKey)
cipherText = cipherKey.encrypt(fp.read())

cipherText = binascii.hexlify(cipherText)

# print(binascii.hexlify(cipherText))

fEnc = open('encrypt.txt', 'wb')
fEnc.write(cipherText)


# archive
#cipherText = pubKey.encrypt(fp.read(),32)
#cipherMsg = cipherText[0]

fPri.close()
fPub.close()
fp.close()
fEnc.close()
