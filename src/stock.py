import pandas as pd

from src.market import *
from src.lib.table_cloms import *


class stock(market):
    us_jp_rate = pd.DataFrame([])

    @staticmethod
    def set_currency_rate():
        tmp_mk = market()
        stock.us_jp_rate = tmp_mk.get_USD_JPY_rate('DEXJPUS').interpolate(limit_direction='both')

    @staticmethod
    def get_currency_rate(init_day=FIRST_DAY, latest_day=TODAY):
        if  stock.us_jp_rate.empty:
            stock.set_currency_rate()
        #return stock.us_jp_rate[stock.us_jp_rate[COL_DATE]>init_day].loc[stock.us_jp_rate[COL_DATE]<latest_day, "DEXJPUS"]
        return stock.us_jp_rate[(stock.us_jp_rate[COL_DATE]>init_day) & (stock.us_jp_rate[COL_DATE]<latest_day)]


    def __init__(self, ticker, data_frame):
        self.ticker_symbole = ticker
        self.amount = data_frame[COL_TRADE_AMOUNT_STOCK].sum()
        self.trade_price = data_frame[COL_TRADE_PRICE_JP].sum()
        self.charge = data_frame[COL_CHARGE_JP].sum()
        self.tax = data_frame[COL_TAX_JP].sum()

        self.book_events=pd.DataFrame([])
        self.book_events[COL_TRADE_DATE] = data_frame[COL_TRADE_DATE].copy()
        self.book_events[COL_AMOUNT_STOCK] = data_frame[COL_TRADE_AMOUNT_STOCK].copy().cumsum()
        self.book_events[COL_TRADE_PRICE_JP] = data_frame[COL_TRADE_PRICE_JP].copy().cumsum()

        if  stock.us_jp_rate.empty:
            stock.set_currency_rate()

    def set_dividend_info(self, data_frame):
        self.dividend_tabale = data_frame.rename(columns={COL_DIV_REC_DATE: COL_DATE})
        # print(self.dividend_tabale)
        self.dividend_tabale = pd.merge(self.dividend_tabale, stock.get_currency_rate(), on=COL_DATE, how='inner')
        self.dividend_tabale[COL_DIV_REC_PRE_PRICE_JP] = self.dividend_tabale[COL_DIB_REC_PRICE] * self.dividend_tabale[COL_RATE_CCY]
        self.dividend_tabale[COL_DIV_CUMSUM_PRICE_JP] = self.dividend_tabale[COL_DIV_REC_PRE_PRICE_JP].cumsum()
        self.dividend = self.dividend_tabale[COL_DIV_REC_PRE_PRICE_JP].sum()


    def calc_price_table(self):
        market_price_table = self.get_close(self.ticker_symbole)
        #market_price_table[COL_DATE] = pd.to_datetime(market_price_table.index.values.tolist(), format="%Y-%m-%d")
        market_price_table[COL_AMOUNT_STOCK] = 0
        market_price_table[COL_TRADE_PRICE_JP] = 0
        # print(market_price_table)
        for index, event in self.book_events.iterrows():
            amount = event[COL_AMOUNT_STOCK]
            trade_price= event[COL_TRADE_PRICE_JP]
            day = event[COL_TRADE_DATE]
            market_price_table.loc[market_price_table[COL_DATE] > day, COL_AMOUNT_STOCK] = amount
            market_price_table.loc[market_price_table[COL_DATE] > day, COL_TRADE_PRICE_JP] = trade_price
        
        market_price_table[COL_DIV_CUMSUM_PRICE_JP] = 0
        for index, event in self.dividend_tabale.iterrows():
            rec_cumsum_price = event[COL_DIV_CUMSUM_PRICE_JP]
            rec_date = event[COL_DATE]
            market_price_table.loc[market_price_table[COL_DATE] > rec_date, COL_DIV_CUMSUM_PRICE_JP] = rec_cumsum_price


        #print(stock.get_currency_rate())
        market_price_table = pd.merge(market_price_table, stock.get_currency_rate(), on=COL_DATE, how='inner')
        market_price_table[COL_PRICE] = market_price_table[COL_CLOSE] * market_price_table[COL_AMOUNT_STOCK]
        market_price_table[COL_PRICE] = (market_price_table[COL_PRICE] * market_price_table[COL_RATE_CCY])
        market_price_table[COL_INTEREST_RATE] =  (market_price_table[COL_PRICE] - (market_price_table[COL_TRADE_PRICE_JP] - market_price_table[COL_DIV_CUMSUM_PRICE_JP])) * 100/ (market_price_table[COL_TRADE_PRICE_JP]-market_price_table[COL_DIV_CUMSUM_PRICE_JP]) 
        self.price_table = market_price_table.reset_index()[[COL_DATE, COL_AMOUNT_STOCK, COL_PRICE, COL_INTEREST_RATE, COL_TRADE_PRICE_JP, COL_DIV_CUMSUM_PRICE_JP]]
        # print(market_price_table)

