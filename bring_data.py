import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from Kiwoom import *
import time
import pandas as pd
import sqlite3

# 주식 정보를 가져오는 클래스
class Bring_stock_data():
    def __init__(self):
        super().__init__()

        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

    # 주식 기본정보를 df로 받는다.
    def load_item_basic_info(self):
        stock_code = input("stock_code: ")
        start_date = input("start_date: ")
        stock_code = str(stock_code)
        start_date = str(start_date)

        self.kiwoom.set_input_value("종목코드", stock_code)
        self.kiwoom.set_input_value("조회일자", start_date)
        self.kiwoom.comm_rq_data("opt10086_req", "opt10086", 0, "0124")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("종목코드", stock_code)
            self.kiwoom.set_input_value("조회일자", start_date)
            self.kiwoom.comm_rq_data("opt10086_req", "opt10086", 2, "0124")

        df = pd.DataFrame(self.kiwoom.ohlcv, columns = ['open', 'high', 'low', 'close', 'volume'], index = self.kiwoom.ohlcv['date'])
        print(df)

        return df

    # df를 csv파일로 저장
    def save_df_to_csv(self, df):
        print("stock_save_to_csv")
        df.to_csv("C:\\Users\\Mark\\PycharmProjects\\Real_Program\\item_basic_info.csv", mode='w')

if __name__ == "__main__":
    print("start program")
    app = QApplication(sys.argv)
    bsd = Bring_stock_data()
    df = bsd.load_item_basic_info()
    bsd.save_df_to_csv(df)

    #
    # codelist = [000030,000030,000030,000030,000030]
    # for i in codelist:
    #     stocksim.stock_save_to_csv(i)
