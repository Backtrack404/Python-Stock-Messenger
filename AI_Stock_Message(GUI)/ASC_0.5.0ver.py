from Scraper import *
from XSL import *
from AI import *
from KeyValue import*
import tkinter
from tkinter import *
from tkinter import messagebox
import time
import threading

def FuncSetData(event):
    global Count
    SetData.config(text="추출 데이터 개수:" + str(DataEntry.get()))
    try:
        if(int(DataEntry.get())<=0):
            messagebox.showwarning("Warning","0이하는 입력 불가능 합니다.")
        else:
            Count = str(int(DataEntry.get()))
            return int(Count)
    except ValueError:
        messagebox.showwarning("Warning","숫자만 입력 가능합니다.")

def FuncSetCode(event):
    global Code
    SetCode.config(text="종목이름:" + str(CodeEntry.get()))
    try:
        Code = stock(CodeEntry.get()) 
    except:
        messagebox.showwarning("Warning",CodeEntry.get() + "는(은) 현재 추가 되어있지 않은 종목입니다.")
    return Code


def FuncSetName(event):
    global Name
    SetName.config(text="파일이름:" + str(NameEntry.get()))
    Name = str(NameEntry.get())


def threadCalculate():
    global calculation_time
    AICOUNT = '720'   
    button1.config(state=tkinter.DISABLED)
    
    startTime = time.time()
    SetResult.config(text="Calculating...")
    SetResult.update()
    result, resDate, markPrice, hiPrice, loPrice, nowPrice, volume = Scraper(int(Count), Code).Scraping() 
    AIresult, AIresDate, AImarkPrice, AIhiPrice, AIloPrice, AInowPrice, AIvolume = Scraper(AICOUNT, Code).Scraping()
    redate, Predict = AI_Stock(AIresDate, AInowPrice).AI_Calc()
    
    for i in range(487,494): 
        resDate.append(redate[i].strftime('%Y%m%d'))
        nowPrice.append(round(Predict[i]))
        
    XSL(resDate, markPrice, hiPrice, loPrice, nowPrice, volume, Name).Xsl()
    
    calculation_time = time.time() - startTime
    print("Calculation time:{0:.3f} sec".format(calculation_time))
    ProcessTime.config(text="연산시간:{0:.3f} sec".format(calculation_time))
    button1.config(state=tkinter.NORMAL)
    Complete()
    
    
def FunctionRefresh():
    try:       
        thread = threading.Thread(target = threadCalculate)
        thread.start()      
        SetResult.config(text="추출 완료")
        
    except NameError:
        messagebox.showwarning("Warning","데이터 입력 후 Enter를 눌러주세요!")
        SetResult.config(text="데이터 입력 후 Enter를 눌러주세요!")
        

def showError():
    messagebox.showwarning("Warning","알수없는 Error!")

def showError_0():
    messagebox.showwarning("Warning","0 이하는 입력할 수 없습니다.")

def Complete():
    lines = ["Complete", "연산시간:{0:.3f} sec".format(calculation_time)]
    messagebox.showinfo("Info",'\n'.join(lines))
    

root = Tk()
root.title("Auto Stock Calculator 0.5.0ver")
root.geometry("400x200+700+300")
root.resizable(False,False)

SetData = Label(root, text = '추출 데이터 개수')
SetData.pack()
DataEntry = Entry(root, width=30)
DataEntry.bind("<Return>", FuncSetData)
DataEntry.pack()

SetCode = Label(root, text = '종목이름')
SetCode.pack() 
CodeEntry = Entry(root, width=30)
CodeEntry.bind("<Return>", FuncSetCode)
CodeEntry.pack()

SetName = Label(root, text = '저장될 파일이름')
SetName.pack() 
NameEntry = Entry(root, width=30)
NameEntry.bind("<Return>", FuncSetName)
NameEntry.pack()

SetResult = Label(root,  text = 'stand-by')
SetResult.pack() 

button1 = Button(root, width=10, text="데이터 추출", overrelief="solid", command=FunctionRefresh)
button1.pack()

ProcessTime = Label(root, text = "연산시간")
ProcessTime.pack()

root.mainloop()