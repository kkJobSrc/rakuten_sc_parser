import os

from src.us_stock import *
from src.graph_creator import *
from src.lib.common import *
from src.lib.graph import *
from src.lib.table_cloms import *

if __name__ == "__main__":
    csv_path = get_input_file_us_stock()
    divid_csv_path = get_input_file_dividend()
    print(csv_path)
    as_of_date = os.path.basename(csv_path).split("_")[-1].split(".")[0]
    
    # Initailize instance
    raw_table = read_download_csv(csv_path, encoding="shift-jis")
    _stock = us_stock(raw_table)

    raw_table = read_download_csv(divid_csv_path, encoding="shift-jis")
    _stock.set_dividend_info(raw_table)
    _stock.set_indivisual_stock()

    # Output graph that is all trade summary
    output_path = os.path.join(OUT_DIR, "all_trade_summary"+ "_" + as_of_date + ".png")
    summary_text = "Tax    : {:,.2f} yen\n".format(_stock.total_tax)
    summary_text += "Charge: {:,.2f} yen\n".format(_stock.total_charge)
    summary_text += "Trade : {:,.2f} yen\n".format(_stock.total_trade_price)
    summary_text += "Dividend: {:,.2f} yen\n".format(_stock.total_dividend)
    summary_text += "Total pay: {:,.2f} yen\n".format(_stock.total_trade_price + _stock.total_charge + _stock.total_tax)
    summary_text += "Total : {:,.2f} yen".format(_stock.total_trade_price + _stock.total_charge + _stock.total_tax - _stock.total_dividend)
    us_stock_graph = graph_creator(second_y_ax=True)
    us_stock_graph.set_color_variation(5) # tax, charge and trade price
    us_stock_graph.plot_cumsum(_stock.trade_table)
    us_stock_graph.plot_divend_cumsum(_stock.dividend_summary_tabale)
    us_stock_graph.set_text_box(text=summary_text, pos_x=FIRST_DAY, pos_y=2500000, font_size=12)
    us_stock_graph.save_figure(output_path, "Trade summary", "Date", "Trade price[Yen]", "Tax/charge [Yen]")

    inv_stock_graph = multi_graph_creator(len(_stock.indivisual_stock) + 1)
    graph_base.set_color_counter_zero()

    inv_stock_graph.plot_price_table(_stock.summary_price_table, 0, "Summary", COL_PRICE)
    inv_stock_graph.plot_table_second_ax(_stock.summary_price_table, 0, COL_INTEREST_RATE)
    # print(_stock.summary_price_table)

    for i, key in enumerate(_stock.indivisual_stock):
        print(key) 
        print("- Amount: ", _stock.indivisual_stock[key].amount)
        print("- Price :", _stock.indivisual_stock[key].trade_price)
        print("- Charge:", _stock.indivisual_stock[key].charge)
        print("- Dividend:", _stock.indivisual_stock[key].dividend )
        # print("- Tax   :", _stock.indivisual_stock[key].tax)
        # print("- Event tab.:", _stock.indivisual_stock[key].book_events)
        # print("- Price tab.:", _stock.indivisual_stock[key].price_table)
        # print(_stock.get_time_increase(_stock.trade_table, 
        #                               [COL_TRADE_DATE, COL_TRADE_AMOUNT_STOCK, COL_TRADE_PRICE_JP,
        #                                COL_CHARGE_JP,COL_TRADE_PRICE_JP], ticker=key))

        inv_stock_graph.plot_price_table(_stock.indivisual_stock[key].price_table, i+1, key, COL_PRICE)
        inv_stock_graph.plot_table_second_ax(_stock.indivisual_stock[key].price_table, i+1, COL_INTEREST_RATE)

    inv_stock_graph.save_figure( os.path.join(OUT_DIR, "inv_stocs_" + as_of_date + ".png"), "Inv. stocks ")