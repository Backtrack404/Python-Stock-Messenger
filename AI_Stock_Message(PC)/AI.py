from Scraper import *
from XSL import *
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet.forecaster import Prophet

# AI_Stock 클래스
class AI_Stock:
    # AI_Stock은 2년치 날짜와 시장가를 넘겨받습니다.(종가)
    def __init__(self, resDate, markPrice):
        self.__resDate = resDate
        self.__markPrice = markPrice
    
    def AI_Calc(self):    
        ds = [] # 날짜에 쓰일 변수
        format = '%Y-%m-%d' # 날짜 포멧 형식(고정이니 바꾸지 마세요)
        for i in range(len(self.__resDate)):  #날짜 포멧 변경 루프문입니다. (%Y%m%d -> %Y-%m-%d)
            tmp = self.__resDate[i][:4]+'-'+self.__resDate[i][4:6]+"-"+self.__resDate[i][6:8]
            dt_datetime = datetime.strptime(tmp,format)
            ds.append(dt_datetime)


        m = Prophet() # 시계열 예측 분석 알고리즘
        #날짜와 가격을 넘겨주면 연산
        prophet_series = pd.DataFrame(list(zip(ds, self.__markPrice)),columns=('ds','y'))  
        m.fit(prophet_series)

        # periods 수정시 telegram_msg make_file for문 범위 변경!
        future =  m.make_future_dataframe(periods=7)  # 2년치 데이터를 기반으로 1주일치 예측 
        forecast = m.predict(future) # 예측 시작
        retPredict = forecast['ds'], forecast['yhat'] # 결과 
        #fig, ax = plt.subplots(figsize=(16,5))
        # plt.plot(forecast['ds'].dt.to_pydatetime(),forecast['yhat'], label='forecast', color='blue')
        # plt.plot(prophet_series['ds'].dt.to_pydatetime(),prophet_series['y'], label='observations ', color='black')
        # plt.fill_between(forecast['ds'].dt.to_pydatetime(), forecast['yhat_upper'],forecast['yhat_lower'],color='skyblue',label='80% confidence interval')
        # plt.legend()
        # plt.xlabel('date')
        # plt.ylabel('price(WON)')
        # plt.show()
        return retPredict # 결과 반환
    