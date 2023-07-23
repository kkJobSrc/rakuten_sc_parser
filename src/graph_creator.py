import numpy as np
from src.lib.graph import graph_base
from src.lib.graph import multi_graph
from src.lib.table_cloms import *


class graph_creator(graph_base):
    def __init__(self, width=11.67, height=8.47, bpi=100, second_y_ax=False):
        super().__init__(width, height, bpi, second_y_ax)
        graph_base.set_color_counter_zero()

    def plot_and_scatter(self, ax, x, y, _label="",_ls="-"):
        color_num = graph_base.get_color_counter()
        ax.plot(x, y, label=_label, color=self.colors[color_num], ls=_ls)
        ax.scatter(x, y, color=self.colors[color_num])


    def plot_cumsum(self, data_frame):
        self.plot_and_scatter(self.ax1, data_frame[COL_TRADE_DATE],
                               data_frame[COL_CUMSUM_TRADE_PRICE_JP], 
                               _label="Trade Price"
                               )

        self.plot_and_scatter(self.ax2, data_frame[COL_TRADE_DATE],
                              data_frame[COL_CUMSUM_CHARGE_JP],
                              _label="Charge", _ls ="--"
                              )

        self.plot_and_scatter(self.ax2, data_frame[COL_TRADE_DATE],
                              data_frame[COL_CUMSUM_TAX_JP],
                              _label="Tax", _ls="--"
                              )

    def plot_divend_cumsum(self, data_frame):
        self.plot_and_scatter(self.ax2, data_frame[COL_DATE],
                               data_frame[COL_DIV_CUMSUM_PRICE_JP], 
                               _label="Dividend", _ls="--"
                               )


class multi_graph_creator(multi_graph):
    def __init__(self, graph_num, col_num=1, dpi=100):
        super().__init__(graph_num, col_num, dpi)


    def plot_graph(self, ax, x, y, _label="", _ls="-"):
        color_num = graph_base.get_color_counter()
        self.set_monthly_tics(ax)
        ax.plot(x, y, label=_label, color=self.colors[color_num], ls=_ls)


    def plot_price_table(self, data_frame, graph_num, ticker, col):
        label = ticker + " price[Yen]"
        self.plot_graph(self.ax_list[graph_num], data_frame[COL_DATE], data_frame[col].replace([0], np.nan), label)
        self.ax_list[graph_num].set_ylabel(label)
        self.ax_list[graph_num].set_xlabel("Date")
        

    def plot_table_second_ax(self, data_frame, graph_num, col, ymin=-30, ymax=30):
        label = "Interest rate[%]"
        ax2 = self.ax_list[graph_num].twinx()
        self.plot_graph(ax2, data_frame[COL_DATE], data_frame[col].replace([0], np.nan), label, "--")
        ax2.set_ylabel(label)
        ax2.set_ylim([ymin,ymax])
        ax2.grid()
        graph_base.set_color_counter_zero()


        #print(data_frame[col])