from Scraper import *
from XSL import *
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet.forecaster import Prophet

class AI_Stock:
    def __init__(self, resDate, markPrice):
        self.__resDate = resDate
        self.__markPrice = markPrice
    
    def AI_Calc(self):    
        ds = []
        format = '%Y-%m-%d'
        for i in range(len(self.__resDate)):
            tmp = self.__resDate[i][:4]+'-'+self.__resDate[i][4:6]+"-"+self.__resDate[i][6:8]
            dt_datetime = datetime.strptime(tmp,format)
            ds.append(dt_datetime)


        m = Prophet()
        prophet_series = pd.DataFrame(list(zip(ds, self.__markPrice)),columns=('ds','y'))
        m.fit(prophet_series)

        # periods 수정시 telegram_msg make_file for문 범위 변경!
        future =  m.make_future_dataframe(periods=7) 
        forecast = m.predict(future)
        retPredict = forecast['ds'], forecast['yhat']
        #fig, ax = plt.subplots(figsize=(16,5))
        # plt.plot(forecast['ds'].dt.to_pydatetime(),forecast['yhat'], label='forecast', color='blue')
        # plt.plot(prophet_series['ds'].dt.to_pydatetime(),prophet_series['y'], label='observations ', color='black')
        # plt.fill_between(forecast['ds'].dt.to_pydatetime(), forecast['yhat_upper'],forecast['yhat_lower'],color='skyblue',label='80% confidence interval')
        # plt.legend()
        # plt.xlabel('date')
        # plt.ylabel('price(WON)')
        # plt.show()
        return retPredict
    