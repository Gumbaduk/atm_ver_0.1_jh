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
        self.kiwoom.df_10001 = {'code': [], 'name': [], 'month': [], 'face_value': [], 'capital': []}
        self.kiwoom.df_10002 = {'code': [], 'name': [], '매도거래원명1': [], '매도거래원1': [], '매도거래량1': [], '매수거래원명1': [], '매수거래원1': [], '매수거래량1': []}
        self.kiwoom.df_10003 = {'시간': [], '현재가': [], '누적거래량': []}
        self.kiwoom.df_10004 = {'총매도잔량': [], '총매수잔량': [], '시간외매도잔량': [], '시간외매수잔량': []}
        self.kiwoom.df_10005 = {'날짜': [], '시가': [], '고가': [], '저가': [], '종가': []}
        self.kiwoom.df_10006 = {'날짜': [], '시가': [], '고가': [], '저가': [], '종가': []}
        self.kiwoom.df_20006 = {'일자': [], '시가': [], '고가': [], '저가':[]}

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
        print("save_to_csv")
        df.to_csv("C:\\workplace\\atm_project\\atm_ver_0.1_jh\\item_basic_info.csv", mode='w')

        return df

    def get_tr10001_data(self):
        stock_code = input("stock_code: ")
        stock_code = str(stock_code)

        self.kiwoom.set_input_value("종목코드", stock_code)
        self.kiwoom.comm_rq_data("opt10001_req", "opt10001", 0, "0286")

        print(self.kiwoom.df_10001)

        df = pd.DataFrame(self.kiwoom.df_10001, columns = ['name', 'month', 'face_value', 'capital'], index = self.kiwoom.df_10001['code'])
        print(df)
        print("save_to_csv")
        df.to_csv("C:\\workplace\\atm_project\\atm_ver_0.1_jh\\tr10001.csv", mode='w')

    def get_tr10002_data(self):
        stock_code = input("stock_code: ")
        stock_code = str(stock_code)

        self.kiwoom.set_input_value("종목코드", stock_code)
        self.kiwoom.comm_rq_data("opt10002_req", "opt10002", 0, "0129")

        print(self.kiwoom.df_10002)
        df = pd.DataFrame(self.kiwoom.df_10002, columns = ['name', '매도거래원명1', '매도거래원1', '매도거래량1', '매수거래원명1', '매수거래원1', '매수거래량1'], index= self.kiwoom.df_10002['code'])
        print(df)
        print("save_to_csv")
        df.to_csv("C:\\workplace\\atm_project\\atm_ver_0.1_jh\\tr10002.csv", mode='w')

    def get_tr10003_data(self):
        stock_code = input("stock_code: ")
        stock_code = str(stock_code)

        self.kiwoom.set_input_value("종목코드", stock_code)
        self.kiwoom.comm_rq_data("opt10003_req", "opt10003", 0, "0120")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("종목코드", stock_code)
            self.kiwoom.comm_rq_data("opt10003_req", "opt10003", 2, "0120")

        print(self.kiwoom.df_10003)
        df = pd.DataFrame(self.kiwoom.df_10003, columns = ['현재가', '누적거래량'], index= self.kiwoom.df_10003['시간'])
        print(df)
        print("save_to_csv")
        df.to_csv("C:\\workplace\\atm_project\\atm_ver_0.1_jh\\tr10003.csv", mode='w')

    def get_tr10004_data(self):
        stock_code = input("종목코드: ")
        stock_code = str(stock_code)


        self.kiwoom.set_input_value("종목코드", stock_code)
        self.kiwoom.comm_rq_data("opt10004_req", "opt10004", 0, "0119")

        df = pd.DataFrame(self.kiwoom.df_10004, columns = ['총매도잔량', '총매수잔량', '시간외매도잔량', '시간외매수잔량'])
        print(df)
        print("save_to_csv")
        df.to_csv("C:\\workplace\\atm_project\\atm_ver_0.1_jh\\tr10004.csv", mode='w')

    def get_tr10005_data(self):
        stock_code = input("종목코드: ")
        stock_code = str(stock_code)


        self.kiwoom.set_input_value("종목코드", stock_code)
        self.kiwoom.comm_rq_data("opt10005_req", "opt10005", 0, "0124")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("종목코드", stock_code)
            self.kiwoom.comm_rq_data("opt10005_req", "opt10005", 2, "0124")

        df = pd.DataFrame(self.kiwoom.df_10005, columns = ['시가', '고가', '저가', '종가'], index= self.kiwoom.df_10005['날짜'])
        print(df)
        print("save_to_csv")
        df.to_csv("C:\\workplace\\atm_project\\atm_ver_0.1_jh\\tr10005.csv", mode='w')

    def get_tr10006_data(self):
        stock_code = input("종목코드: ")
        stock_code = str(stock_code)


        self.kiwoom.set_input_value("종목코드", stock_code)
        self.kiwoom.comm_rq_data("opt10006_req", "opt10006", 0, "0124")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("종목코드", stock_code)
            self.kiwoom.comm_rq_data("opt10006_req", "opt10006", 2, "0124")

        df = pd.DataFrame(self.kiwoom.df_10006, columns = ['시가', '고가', '저가', '종가'], index= self.kiwoom.df_10006['날짜'])
        print(df)
        print("save_to_csv")
        df.to_csv("C:\\workplace\\atm_project\\atm_ver_0.1_jh\\tr10006.csv", mode='w')


    def get_tr20006_data(self):
        market_code = input("업종코드: ")
        start_date = input("기준일자: ")
        market_code = str(market_code)
        start_date = str(start_date)

        self.kiwoom.set_input_value("업종코드", market_code)
        self.kiwoom.set_input_value("기준일자", start_date)
        self.kiwoom.comm_rq_data("opt20006_req", "opt20006", 0, "0602")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("업종코드", market_code)
            self.kiwoom.set_input_value("기준일자", start_date)
            self.kiwoom.comm_rq_data("opt20006_req", "opt20006", 2, "0602")

        df = pd.DataFrame(self.kiwoom.df_20006, columns = ['시가', '고가', '저가'], index = self.kiwoom.df_20006['일자'])
        print(df)
        print("save_to_csv")
        df.to_csv("C:\\workplace\\atm_project\\atm_ver_0.1_jh\\tr20006.csv", mode='w')

    # df를 csv파일로 저장
    def save_df_to_csv(self, df):
        print("stock_save_to_csv")
        df.to_csv("C:\\workplace\\atm_project\\atm_ver_0.1_jh\\item_basic_info.csv", mode='w')

if __name__ == "__main__":
    print("start program")
    app = QApplication(sys.argv)
    bsd = Bring_stock_data()
    # df = bsd.load_item_basic_info()
    # bsd.save_df_to_csv(df)
    bsd.get_tr10006_data()


    #
    # codelist = [000030,000030,000030,000030,000030]
    # for i in codelist:
    #     stocksim.stock_save_to_csv(i)
