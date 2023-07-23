
import glob
import os
import pandas_datareader as pdr
import pandas as pd
import time

from src.lib.table_cloms import *
from src.lib.common import *


class market():
    # Returen transaction file name
    def get_transaction_name(self, tiker):
        return tiker + "_" +  TODAY.strftime("%Y_%m_%d") 


    ## Remove old transaction file
    def remove_old_transaction(self, tiker):
        old_files = glob.glob(os.path.join(TRANSACTION_DIR, tiker+"_*"))
        for file_path in old_files:
            os.remove(file_path)

    def save_transaction_file(self, path, ticker, init_day, latest_day, key, api_src):
            if not(os.path.isfile(path)):
                create_new_dir(os.path.dirname(path))
                self.remove_old_transaction(ticker)
                pdr.DataReader(ticker, api_src, end=latest_day, start=init_day, api_key=key).rename(columns = str.upper).to_csv(path)
                print(ticker+": read from API")
                time.sleep(API_COOL_TIME) # To keep within access par time  bounds(200 access/min)


    ## Get market price  form transction file or API
    def get(self, tiker, init_day=FIRST_DAY, latest_day=TODAY, key=APIKEY, src= "stooq"):
        try:
            history_data_path = os.path.join(TRANSACTION_DIR, self.get_transaction_name(tiker)+".csv")
            self.save_transaction_file(history_data_path, tiker, init_day, latest_day, key, src)

            raw_table = pd.read_csv(history_data_path, header=0, encoding="utf-8", thousands=',').rename(columns = str.upper)
            raw_table[COL_DATE] = pd.to_datetime(raw_table[COL_DATE], format="%Y-%m-%d")
        except  Exception as e:
            print("Failed to get martket table...")
            print("message:{0}".format(e.message))
            raw_table = pd.DataFrame([])
        finally:
            #print(raw_table)
            return raw_table


    ## Extract market price data from table  
    def get_col(self, tiker, init_day, latest_day, col_name):
        data = self.get(tiker, init_day, latest_day)
        col_num_upper = col_name.upper()
        return data[[COL_DATE, col_num_upper]] if col_num_upper in data.columns else None


    ## Get market close price
    def get_close(self, tiker, init_day=FIRST_DAY, latest_day=TODAY):
        return self.get_col(tiker, init_day, latest_day, "close")

    ## Get USD JPY 
    def get_USD_JPY_rate(self, ccy, init_day=FIRST_DAY, latest_day=TODAY):
        return self.get(ccy, init_day, latest_day, src='fred').rename({ccy:COL_RATE_CCY},axis=1)

