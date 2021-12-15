from Scraper import *
from XSL import *
from AI import *
from KeyValue import*
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet.forecaster import Prophet

# Fitting된 최적화 값입니다 바꾸지 마세요
AICOUNT = '720'   

#여기부터 본 코드 시작
if __name__ == '__main__': 

    print("종목 추출 갯수: ")
    count = int(input())
   
    print("추출 종목 이름: ")
    getcode = input()
    
    # KeyValue.py에 stock()함수 있습니다. 
    # Key-Value 쌍으로 존재하며 종목이름에 따른 종목 코드를 반환합니다.
    # 아직 몇개 없어서 추가해야합니다. 
    code = stock(getcode)   
    # XML에서 일별로 받아옵니다. (하루하루 최종값을 가져옴)
    # 현재 날짜 - 종목 추출 갯수 부터 오늘까지 받아옵니다.   
    timeframe = "day"
    
    
    
    # Sceaper클래스는 Sceaper.py에 존재하며 사용자가 입력한 값들을 바탕으로 네이버 주식 XML을 파싱해옵니다. 
    # Sceaper클래스 안에있는 Scraping() 함수에서 result, resDate, markPrice, hiPrice, loPrice, nowPrice, volume을 반환합니다.
    result, resDate, markPrice, hiPrice, loPrice, nowPrice, volume = Scraper(count, code).Scraping() #
    # AI연산을 위해 2년치 분을 따로 받아옵니다.
    AIresult, AIresDate, AImarkPrice, AIhiPrice, AIloPrice, AInowPrice, AIvolume = Scraper(AICOUNT, code).Scraping()
    # AI_Stock 클래스는 AI.py에 존재하며 AI_Calc는 retPredict를 반환
    # retPredict는 미래 날짜와 예측 가격으로 이루어져 있어 redate에는 미래 날짜가 들어가고 Predict에는 미래 예측가가 들어갑니다. 
    redate, Predict = AI_Stock(AIresDate, AInowPrice).AI_Calc()    
    
    # 범위는 인공지능에 최적화된 fitting값입니다. 바꾸지 마세요
    # resDate(XML에서 파싱한 기간)에 인공지능에서 예측한 미래 날짜를 추가시킵니다.
    # nowPrice(XML에서 파싱한 가격)에 인공지능에서 예측한 미래 가격을 추가시킵니다.  
    for i in range(487,494): 
       resDate.append(redate[i].strftime('%Y%m%d'))
       nowPrice.append(round(Predict[i]))

    
    # Xsl(result)
    # print("결과 반환:", result)
    # print("resDate 반환:", resDate)
    # print("markPric 반환:", markPric)
    # print("hiPrice 반환:", hiPrice)
    # print("loPrice 반환:", loPrice)
    # print("nowPrice 반환:", nowPrice)
    # print("volume 반환:", volume)
    
    # name은 xsl파일 저장시에 사용할 이름입니다. 여러번 받아와도 중복되지 않게 년-월-일-시-분-초 로 이름이 지어집니다. 
    name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')  
    # XSL 클래스는 XSL.py에 있으며 Xsl()함수를 통해 엑셀로 변환시킵니다. 
    XSL(resDate, markPrice, hiPrice, loPrice, nowPrice, volume, name).Xsl()


