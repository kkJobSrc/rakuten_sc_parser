import pandas as pd
import numpy as np

from src.stock import *
from src.market import * 
from src.lib.table_cloms import *

WHERE_DIV_MARKET = '米国株式'

class us_stock():
    SELECT_COL_NAMES = [
                        COL_TRADE_DATE,
                        COL_TICKER, 
                        COL_TRADE_AMOUNT_STOCK,
                        COL_BUY_SELL_SYMBOLE, 
                        COL_TRADE_PRICE_US,
                        COL_RATE,
                        COL_TAX_US,
                        COL_CHARGE_US,
                        COL_FINAL_PRICE_US,
                        COL_FINAL_PRICE_JP
                        ]

    SELECT_DIV_COL_NAMES = [
                        COL_DIV_REC_DATE,
                        COL_DIV_TICKER,
                        COL_DIV_MARKET,
                        COL_DIB_REC_PRICE
                        ]

    ## Calc cumulative sum of same ticker from initial day to today(lateat put day)
    def get_time_increase(self, data_frame, colmums, ticker="", first_time=FIRST_DAY, end_time=TODAY):
        if ticker:
            ex_data_frame = data_frame[data_frame[COL_TICKER]==ticker].copy()

        ex_data_frame = ex_data_frame.loc[ (first_time < data_frame[COL_TRADE_DATE]) , colmums].copy()
        return ex_data_frame.cumsum()


    ## convert USD to JPY
    def convert_us_to_yen(self, data_frame, col):
        #print(data_frame.values)
        return float(data_frame[col]) * data_frame[COL_RATE]


    ## Attach sing price (When call=+ / put =-)
    def attach_sign_price(self):
        singanl_col = np.where(self.trade_table[COL_BUY_SELL_SYMBOLE] == VALUE_CALL, 1, -1)
        self.trade_table[COL_TRADE_PRICE_US] = self.trade_table[COL_TRADE_PRICE_US] * singanl_col
        self.trade_table[COL_FINAL_PRICE_US] = self.trade_table[COL_FINAL_PRICE_US] * singanl_col
        self.trade_table[COL_FINAL_PRICE_JP] = self.trade_table[COL_FINAL_PRICE_JP] * singanl_col
        self.trade_table[COL_TRADE_AMOUNT_STOCK] = self.trade_table[COL_TRADE_AMOUNT_STOCK] * singanl_col


    def __init__(self, data_frame) -> None:
        # Initialze data table
        self.trade_table = data_frame[self.SELECT_COL_NAMES]
        trade_date_col = self.trade_table[COL_TRADE_DATE].copy()
        self.trade_table.loc[:,COL_TRADE_DATE]= pd.to_datetime(trade_date_col, format='%Y/%m/%d')
        self.trade_table = self.trade_table.replace("-", 0).fillna(0)        
        self.attach_sign_price()

        # Convert US doll to JP Yen
        self.trade_table[COL_TAX_JP] = self.trade_table.apply(self.convert_us_to_yen, col=COL_TAX_US, axis=1)
        self.trade_table[COL_CHARGE_JP] = self.trade_table.apply(self.convert_us_to_yen, col=COL_CHARGE_US, axis=1)
        self.trade_table[COL_TRADE_PRICE_JP] = self.trade_table.apply(self.convert_us_to_yen, col=COL_TRADE_PRICE_US, axis=1)

        # Calc total price
        self.trade_table[[COL_CUMSUM_TAX_JP, COL_CUMSUM_CHARGE_JP, COL_CUMSUM_TRADE_PRICE_JP]] = self.trade_table.loc[:,[COL_TAX_JP, COL_CHARGE_JP, COL_TRADE_PRICE_JP]].cumsum()
        self.total_tax = self.trade_table[COL_TAX_JP].sum()
        self.total_charge = self.trade_table[COL_CHARGE_JP].sum()
        self.total_trade_price = self.trade_table[COL_TRADE_PRICE_JP].sum()

        # Extract ticker sybole
        self.ticker_syboles = self.trade_table[COL_TICKER].unique()
        self.summary_price_table = pd.DataFrame([])
        self.dividend_summary_tabale = pd.DataFrame([])


    ## Create indivisual stock instance
    def set_indivisual_stock(self):
        self.indivisual_stock = {}
        for ticker in self.ticker_syboles:
            self.indivisual_stock[ticker] = stock(ticker, 
                                                   self.trade_table[self.trade_table[COL_TICKER] == ticker])
            self.indivisual_stock[ticker].set_dividend_info(self.dividend_tabale[self.dividend_tabale[COL_DIV_TICKER] == ticker])
            self.indivisual_stock[ticker].calc_price_table()
            
            if self.summary_price_table.empty:
                self.summary_price_table = self.indivisual_stock[ticker].price_table[[COL_DATE,COL_PRICE,COL_TRADE_PRICE_JP,COL_DIV_CUMSUM_PRICE_JP]].copy()
            else:
                self.summary_price_table[COL_PRICE] += self.indivisual_stock[ticker].price_table[COL_PRICE]
                self.summary_price_table[COL_TRADE_PRICE_JP] += self.indivisual_stock[ticker].price_table[COL_TRADE_PRICE_JP]
                self.summary_price_table[COL_DIV_CUMSUM_PRICE_JP] += self.indivisual_stock[ticker].price_table[COL_DIV_CUMSUM_PRICE_JP]
        
        self.summary_price_table[COL_INTEREST_RATE]  = 0
        self.summary_price_table[COL_INTEREST_RATE] = (self.summary_price_table[COL_PRICE] - 
                                                       (self.summary_price_table[COL_TRADE_PRICE_JP] - self.summary_price_table[COL_DIV_CUMSUM_PRICE_JP]))  * 100 / (self.summary_price_table[COL_TRADE_PRICE_JP] - self.summary_price_table[COL_DIV_CUMSUM_PRICE_JP])



    def set_dividend_info(self, data_frame):
        # Edit original data
        self.dividend_tabale = data_frame[self.SELECT_DIV_COL_NAMES]#.reset_index(inplace= True)
        self.dividend_tabale[COL_DIV_REC_DATE]= pd.to_datetime(self.dividend_tabale[COL_DIV_REC_DATE], format='%Y/%m/%d')
        self.dividend_tabale = self.dividend_tabale[self.dividend_tabale[COL_DIV_MARKET] == WHERE_DIV_MARKET]

        # Set summary data
        self.dividend_summary_tabale = self.dividend_tabale.groupby(COL_DIV_REC_DATE).agg({COL_DIB_REC_PRICE: 'sum'}) # Convine same date Price
        self.dividend_summary_tabale[COL_DATE] = self.dividend_summary_tabale.index
        self.dividend_summary_tabale = pd.merge(self.dividend_summary_tabale, stock.get_currency_rate(), on=COL_DATE, how='inner')
        self.dividend_summary_tabale[COL_DIV_REC_PRE_PRICE_JP] = self.dividend_summary_tabale[COL_DIB_REC_PRICE] * self.dividend_summary_tabale[COL_RATE_CCY]
        self.dividend_summary_tabale[COL_DIV_CUMSUM_PRICE_JP] = self.dividend_summary_tabale[COL_DIV_REC_PRE_PRICE_JP].cumsum()
        self.total_dividend = self.dividend_summary_tabale[COL_DIV_REC_PRE_PRICE_JP].sum()
        #print(self.dividend_summary_tabale, ccy_rate[COL_RATE_CCY])
        
    