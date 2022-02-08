import sys
import pymysql
import numpy as np

host = 'kkada-dev.ctprpuwvyaac.ap-northeast-2.rds.amazonaws.com'
port = int(3306)
user = 'admin'
passwd = 'kgo100dk23!'
database = 'kkada_back'
autocommit = False

class DataBase:
    def connectDB():
        try:
            conn = pymysql.connect(user = user, password = passwd, host = host,
                                   port = port, database = database, autocommit = autocommit)
            print("connection to DB")
        except pymysql.Error as error:
            print(f"Error connection to DB : {error}")
            sys.exit(1)
        return conn
    
            
    def getUseDocData(pinId):
        conn = DataBase.connectDB()

        cur = conn.cursor()
        sql_query_m = f"SELECT * FROM kkada_back.task where pinId = '{pinId}';"
    
        cur.execute(sql_query_m)
        rowList = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        
        rowArray = np.array(rowList)
        row = rowArray.reshape(-1)
        print(row[1])
        return row[1]
           

# DataBase.getUseDocData()