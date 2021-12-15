from Scraper import *
from XSL import *
from AI import *
from KeyValue import*
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet.forecaster import Prophet
import os 

AICOUNT = '720'

if __name__ == '__main__':
   abspath = os.path.abspath("./2021_11_23_21_15_23.xlsx")
   print(abspath)
   print("종목 추출 갯수: ")
   count = '15'
   # print("종목 코드: ")
   getcode = input()
   #print(stock(getcode))
   code = stock(getcode)
   
   print("timeframe: ")
   timeframe = "minute"
   
   
   result, resDate, markPrice, hiPrice, loPrice, nowPrice, volume = Scraper(count, code).Scraping()
   AIresult, AIresDate, AImarkPrice, AIhiPrice, AIloPrice, AInowPrice, AIvolume = Scraper(AICOUNT, code).Scraping()
   
   redate, Predict = AI_Stock(AIresDate, AInowPrice).AI_Calc()    
   
   #print(redate[496])
   
   #reversDate = redate[::-1]
   #reversPredict = Predict[::-1]
   
   
   for i in range(487,496):
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
   XSL(resDate, markPrice, hiPrice, loPrice, nowPrice, volume).Xsl()