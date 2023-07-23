
def attach_zenkaku_square_brackets(in_str):
    return "［" + in_str + "］"

def attach_hankaku_square_brackets(in_str):
    return "[" + in_str + "]"


def attach_unit(in_str, unit, zenkaku=True):
    res= ""
    if zenkaku:
        res = in_str + attach_zenkaku_square_brackets(unit)
    else:
        res = in_str + attach_hankaku_square_brackets(unit)

    return res

### Trade History CSV ##
# Colnum name base
COL_TRADE_DATE = "約定日"
COL_TICKER = "ティッカー"
COL_BUY_SELL_SYMBOLE = "売買区分"
COL_TRADE_SYBOLE = "取引"
COL_TRADE_AMOUNT = "数量" 
COL_CHARGE = "手数料"
COL_RATE = "為替レート"
COL_TAX = "税金"
COL_TRADE_PRICE = "約定代金"
COL_FINAL_PRICE = "受渡金額"
COL_FUND_NAME = "ファンド名"


# Colnum unit
UNIT_JP_CURRENCY = "円"
UNIT_US_CURRENCY = "USドル"
UNIT_FUND_AMOUNT = "口"
UNIT_STOCK_AMOUNT = "株"

# Colnum suffix
SUFFIX_LOCAL_CURENCY = "現地通貨"
SUFFIX_USED_RAKUTEN_POINT = "\(ポイント利用)"

# Custum colnum name
COL_TRADE_PRICE_US = attach_unit(COL_TRADE_PRICE, UNIT_US_CURRENCY) # 約定代金［USドル］
COL_TRADE_AMOUNT_STOCK = attach_unit(COL_TRADE_AMOUNT, UNIT_STOCK_AMOUNT) # 数量［株］
COL_TRADE_AMOUNT_FUND = attach_unit(COL_TRADE_AMOUNT, UNIT_FUND_AMOUNT) # 数量［口］
COL_CHARGE_US = attach_unit(COL_CHARGE, UNIT_US_CURRENCY) # 手数料［USドル］
COL_TAX_US = attach_unit(COL_TAX, UNIT_US_CURRENCY) # 税金［USドル］
COL_FINAL_PRICE_US = attach_unit(COL_FINAL_PRICE, UNIT_US_CURRENCY) # 受渡金額［USドル］
COL_FINAL_PRICE_JP = attach_unit(COL_FINAL_PRICE, UNIT_JP_CURRENCY) # 受渡金額［円］

# Detect put or call flag
VALUE_PUT = "売付"
VALUE_CALL = "買付"

# original colnum names
COL_TAX_JP = "TAX_JP"
COL_CHARGE_JP = "CHARGE_JP"
COL_TRADE_PRICE_JP = "TRADE_PRICE_JP"

# cumulative sum
COL_CUMSUM_TAX_JP = "CUMSUM_TAX_JP"
COL_CUMSUM_CHARGE_JP = "CUMSUM_CHARGE_JP"
COL_CUMSUM_TRADE_PRICE_JP = "CUMSUM_TRADE_PRICE_JP"

# For matket table
COL_CLOSE = "CLOSE"
COL_AMOUNT_STOCK = "AMOUNT_STOCK"
COL_DATE = "DATE"
COL_PRICE = "PRICE"
COL_RATE_CCY = "RATE"
COL_INTEREST_RATE = "INTEREST_RATE"

### Dividend History CSV ##
COL_DIV_REC_DATE = "入金日"
COL_DIV_TICKER = "銘柄コード"
COL_DIV_REC_PRE_PRICE = "受取金額" #[円/現地通貨]
COL_DIV_MARKET = "商品"

COL_DIB_REC_PRICE = attach_unit(COL_DIV_REC_PRE_PRICE, UNIT_JP_CURRENCY + "/" + SUFFIX_LOCAL_CURENCY, False)

COL_DIV_REC_PRE_PRICE_JP = "DIV_REC_PRE_PRICE_JP"
COL_DIV_CUMSUM_PRICE_JP = "DIV_CUSUM_PRICE_JP"
