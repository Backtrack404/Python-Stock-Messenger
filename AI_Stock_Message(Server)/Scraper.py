import urllib.request
import xml.etree.ElementTree as ET
import numpy as np
from numpy.core.records import array
import pandas as pd
from datetime import datetime, timedelta 

# 네이버 주식 XML에서 스크래핑 해오는 클래스 입니다.
class Scraper:
    def __init__(self, getCount, getCode, getTimeFrame = "day"): 
        self.__getCount = getCount  # 스크래핑할 갯수
        self.__getCode = getCode # 종목 코드
        # 분, 시, 일 , 주, 월, 년 이 있습니다. 그 중 일별로 받아옵니다.
        self.__getTimeFrame = getTimeFrame 

    def Scraping(self):
        # temp[0] = 날짜    = resDate
        # temp[1] = 시가    = markPric
        # temp[2] = 고가    = hiPrice
        # temp[3] = 저가    = loPrice
        # temp[4] = 현재가  = nowPrice
        # temp[5] = 거래량  = volume
        
        count = str(self.__getCount)
        code = str(self.__getCode)
        timeframe = str(self.__getTimeFrame)
        global Error

        now = datetime.now()
        GetDate = now + timedelta(days=-int(count)) # 크롤링 시작할 날짜 
        GetStartDate = GetDate.strftime('%Y%m%d') # 날짜 포멧 형식(고정 바꾸지 마세요)
        date = str(GetStartDate)
        url = f'https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe={timeframe}&count={count}&requestType=0'
        # print(url) 
        
        # 여기서부터 스크래핑 시작. 위에 배열에 따른 설명 써놨습니다.
        r = urllib.request.urlopen(url)  
        xml_data = r.read().decode('EUC-KR') 
        try: 
            root = ET.fromstring(xml_data)
        except Exception as ex:
            Error = "ErrorCode 1"
        result = []
        resDate = [] 
        markPric = [] 
        hiPrice = []
        loPrice =[]
        nowPrice = [] 
        volume = []
        for index, each in enumerate(root.findall('.//item')):
            temp = each.attrib['data'].split('|')

            if str(temp[1]) == 'null':
                temp[1] = None
            else: 
                temp[1] = int(temp[1])
            
            if str(temp[2]) == 'null':
                temp[2] = None
            else: 
                temp[2] = int(temp[2])
            
            if str(temp[3]) == 'null':
                temp[3] = None
            else: 
                temp[3] = int(temp[3])
            
            if int(temp[4]) == 0:
                temp[4] = None
            else: 
                temp[4] = int(temp[4])
            temp[5] = int(temp[5])
            
            if int(temp[0][0:8]) < int(date):
                continue
            result.append(temp)
            resDate.append(temp[0])
            markPric.append(temp[1])
            hiPrice.append(temp[2])
            loPrice.append(temp[3])
            nowPrice.append(temp[4])
            volume.append(temp[5])
        # for i in range(len(result)):            # 세로 크기
        #     for j in range(len(result[i])):     # 가로 크기
        #         print(result[i][j], end=' ')
        #     print()
        return result, resDate, markPric, hiPrice, loPrice, nowPrice, volume