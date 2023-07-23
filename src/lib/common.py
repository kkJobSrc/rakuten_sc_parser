from datetime import datetime

import pandas as pd
import json
import os

CONF_PATH = "./conf/config.json"
with open(CONF_PATH) as file:
    config = json.load(file)

# Direcotry info
TRANSACTION_DIR = config["TRANSACTION_DIR"]
OUT_DIR = config["OUT_DIR"]
IN_DIR = config["IN_DIR"]

# Input file base name
INPUT_FILE_BASE_NAME_US_STOCK = config["INPUT_FILE_BASE_NAME_US_STOCK"]
INPUT_FILE_BASE_NAME_DIVIDEND = config["INPUT_FILE_BASE_NAME_DIVIDEND"]

# Market api-key
APIKEY = config["APIKEY"] # Alpha Vantage API KEY

# Graph Config
API_COOL_TIME = 2

# Date
FIRST_DAY = datetime(2021, 4, 1)
TODAY = datetime.today()


MS2S = lambda t_ms: t_ms * 1000

def create_new_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def read_download_csv(file_name, encoding="utf-8"):
    return pd.read_csv(file_name, header=0, encoding=encoding, thousands=',')


def get_latest_file(target_dir, ptn=""):
    try:
        path_list = [target_dir + "/" + file for file in os.listdir(target_dir)] 
    
        if ptn:
            path_list = [file for file in path_list if ptn in file]

        path_list.sort(key=os.path.getctime)
        return path_list[-1]

    except:
        print( __file__, ": Not found us stock iput file(", INPUT_FILE_BASE_NAME_US_STOCK ,"*)")



def get_input_file_us_stock()->str:
    try:
        return get_latest_file(IN_DIR, INPUT_FILE_BASE_NAME_US_STOCK)
    except:
        print( __file__, ": Not found us stock iput file(", INPUT_FILE_BASE_NAME_US_STOCK ,"*)")
    return 

def get_input_file_dividend()->str:
    try:
        return get_latest_file(IN_DIR, INPUT_FILE_BASE_NAME_DIVIDEND)
    except:
        print( __file__, ": Not found us stock iput file(", INPUT_FILE_BASE_NAME_US_STOCK ,"*)")
