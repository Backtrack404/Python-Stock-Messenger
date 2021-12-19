import xml.etree.ElementTree as ET

import numpy as np
from numpy.core.records import array
import pandas as pd
from datetime import datetime, timedelta 
import xlsxwriter

# 엑셀로 바꾸는 코드입니다. 자동으로 엑셀로 변환해 저장합니다.
class XSL:
    def __init__(self, resDate, markPrice, hiPrice, loPrice, nowPrice, volume, name): 
        self.__resDate = resDate
        self.__markPrice = markPrice
        self.__hiPrice = hiPrice
        self.__loPrice = loPrice
        self.__nowPrice = nowPrice
        self.__volume = volume
        self.__name = name
    def Xsl(self):
        self.__name = str(self.__name)

        workbook = xlsxwriter.Workbook(f"{self.__name}.xlsx")
        worksheet = workbook.add_worksheet()
        GraphCount = len(self.__resDate)+1

        worksheet.write(0, 0, '날짜')
        worksheet.write(0, 1, '시가')
        worksheet.write(0, 2, '고가')
        worksheet.write(0, 3, '저가')
        worksheet.write(0, 4, '종가')
        worksheet.write(0, 5, '거래량')
        
        worksheet.write_column('A2', self.__resDate )
        worksheet.write_column('B2', self.__markPrice )
        worksheet.write_column('C2', self.__hiPrice )
        worksheet.write_column('D2', self.__loPrice )
        worksheet.write_column('E2', self.__nowPrice )
        worksheet.write_column('F2', self.__volume )
        
        chart1 = workbook.add_chart({'type': 'line'})

        chart1.add_series({
        'name':       '=Sheet1!$B$1',
        'categories': f'=Sheet1!$A$2:$A${GraphCount}',
        'values':     f'=Sheet1!$B$2:$B${GraphCount}',
        'marker': {'type': 'circle', 'size': 7},
        'data_labels': {'value': True, 'position': 'above'},
        })

        chart1.add_series({
        'name':       '=Sheet1!$C$1',
        'categories': f'=Sheet1!$A$2:$A${GraphCount}',
        'values':     f'=Sheet1!$C$2:$C${GraphCount}',
        'marker': {'type': 'circle', 'size': 7},
        'data_labels': {'value': True, 'position': 'above'},
        })

        chart1.add_series({
            'name':       '=Sheet1!$D$1',
            'categories': f'=Sheet1!$A$2:$A${GraphCount}',
            'values':     f'=Sheet1!$D$2:$D${GraphCount}',
            'marker': {'type': 'circle', 'size': 7},
            'data_labels': {'value': True, 'position': 'above'},
            })
        
        chart1.add_series({
            'name':       '=Sheet1!$E$1',
            'categories': f'=Sheet1!$A$2:$A${GraphCount}',
            'values':     f'=Sheet1!$E$2:$E${GraphCount}',
            'marker': {'type': 'circle', 'size': 7},
            'data_labels': {'value': True, 'position': 'above', 'font': {'name': 'Consolas', 'color': 'red'}},
            })
        

        chart1.set_title ({'name': 'Results of analysis'})
        chart1.set_x_axis({'name': '날짜'})
        chart1.set_y_axis({'name': '가격(원)'})

    #2: Original
        chart1.set_style(2)

        #16 ~ 
        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart('G2', chart1, {'x_scale': 2.5, 'y_scale': 2.0})
        # worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
        workbook.close()
        