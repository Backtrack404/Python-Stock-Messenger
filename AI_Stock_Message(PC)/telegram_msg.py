from os import name
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  
from threading import Thread
from datetime import datetime
from Scraper import *
from XSL import *
from AI import *
from KeyValue import*


access = "Telegram API"
secret = "Telegram API"
myToken = "Telegram Token"

bot_token = 'Telegram bot Token'
bot = telegram.Bot(token=bot_token)

chat_id = 'CHAT ID'

Ai_Fitting_Count = '720'

count = '15'
getcode = '삼성전자'
code = stock(getcode)
timeframe = "day" 

name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') 


#명령어 정의
def help_command(update, context) :
    bot.sendMessage(chat_id=chat_id, text='help msg')
    #bot.sendMessage(chat_id=chat_id, text='Claculate Success! \nsend command : /xsl')
     
def make_file(update, context):
    
    bot.sendMessage(chat_id=chat_id, text='now calculating... \ndo not send message')
    global Ai_Fitting_Count, getcode, timeframe, name
    code = stock(getcode) 
    result, resDate, markPrice, hiPrice, loPrice, nowPrice, volume = Scraper(count, code, timeframe).Scraping()
    AIresult, AIresDate, AImarkPrice, AIhiPrice, AIloPrice, AInowPrice, AIvolume = Scraper(Ai_Fitting_Count, code, timeframe).Scraping()
    redate, Predict = AI_Stock(AIresDate, AInowPrice).AI_Calc()    
    name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    try:
        for i in range(487,494):
            resDate.append(redate[i].strftime('%Y%m%d'))
            nowPrice.append(round(Predict[i]))
            XSL(resDate, markPrice, hiPrice, loPrice, nowPrice, volume, name).Xsl()
        bot.sendDocument(chat_id=chat_id, document=open(f'D:\\Code\\Project\\Python\\{name}.xlsx', 'rb'))
        bot.sendMessage(chat_id=chat_id, text='Calculate Success!')
    except:
        XSL(resDate, markPrice, hiPrice, loPrice, nowPrice, volume, name).Xsl()
        bot.sendMessage(chat_id=chat_id, text='연산 완료!\n상장 2년 미만의 종목은 인공지능 서비스를 지원하지 않습니다.')   
        bot.sendDocument(chat_id=chat_id, document=open(f'D:\\Code\\Project\\Python\\{name}.xlsx', 'rb'))
        
            
# message reply function
def get_message(update, context) :
    #update.message.reply_text("got text")
    #update.message.reply_text(update.message.text)
    global getcode, count, timeframe
    getMsg = update.message.text
    # update.message.reply_text(getcode)
    #print(type(getcode))
    
    #print(getMsg[0:2])
    try:
        if getMsg[0:2] == '기간':
            count = getMsg[3:]
            print(count)
            update.message.reply_text("가져올 기간을 변경합니다.")
         
        
        elif stock(getMsg):
            update.message.reply_text("종목을 변경합니다.")
            getcode = getMsg
        else:
            update.message.reply_text("알 수 없는 오류!")
    except:
        update.message.reply_text("기간 또는 종목 변경 오류!\n문법에 맞지 않는 명령어 입니다.")
        

def send_local_file(update, context):
    global name
    bot.sendDocument(chat_id=chat_id, document=open(f'D:\\Code\\Project\\Python\\{name}.xlsx', 'rb'))

# th1 = Thread(target=make_file)
# def Thread():
#     th1.start()
#     th1.join()
    
#새 메시지 확인
updater = Updater(bot_token, use_context=True)


# 메세지중에서 command 제외
message_handler = MessageHandler(Filters.text & (~Filters.command), get_message) 
updater.dispatcher.add_handler(message_handler)

#Multi Thread


# 응답 커맨드 정의
help_handler = CommandHandler('help', help_command)
updater.dispatcher.add_handler(help_handler)

file_Handler = CommandHandler('xsl', send_local_file)
updater.dispatcher.add_handler(file_Handler)

Clac_Handler = CommandHandler('data', make_file)
updater.dispatcher.add_handler(Clac_Handler)

updater.start_polling(timeout=1, clean=True)
updater.idle()