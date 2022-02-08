from fileinput import filename
import boto3
from zipfile import ZipFile

class S3:
    def getS3(certName):
        bucket = "kkayo-private"

        s3 = boto3.client('s3', aws_access_key_id="AKIAZYKPK4MWZNBYKG4L" , aws_secret_access_key="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")

        s3.download_file(bucket, f'{certName}', f'D:\\Code\\Project\\SSL_Socket\\PythonSSL\\{certName}.zip')
        # obj = s3.Object(bucket, '1642398591053-824277250')
        # obj.get()['Body'].read().decode('utf-8') 
        
    def unzip(certi_company,certi_name):
        zip_file = f'D:\\Code\\Project\\SSL_Socket\\PythonSSL\\{certi_name}.zip'
        password = '123123'

        with ZipFile(zip_file) as zf:
          zf.extractall(f'C:\\Users\\Server\\AppData\\LocalLow\\NPKI\\{certi_company}\\USER\\{certi_name}\\', pwd=bytes(password,'utf-8'))


    def unzipTest(certi_company,certi_name):
        zip_file = f'/Users/strelka/Programming/회사/Project/Code/Project/SSL_Socket/PythonSSL/{certi_name}.zip'

        with ZipFile(zip_file) as zf:
          zf.extractall(f'/Users/strelka/Programming/회사/Project/Code/Project/SSL_Socket/{certi_company}/USER/{certi_name}/')
        

# getS3()
certi_company = "test_comp"
certi_name = "test"

S3.unzipTest(certi_company, certi_name)