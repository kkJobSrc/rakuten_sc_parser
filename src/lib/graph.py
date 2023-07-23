
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import os
import random

from src.lib.common import *

BASE_COLORS = ["red","green","blue","darkviolet","orangered", "aqua", "lime"]
DATE_PATARN = '%Y-%m'
TEXT_BOX_STYLE = {
    "facecolor" : "azure",
    "edgecolor" : "lightcyan",
    "linewidth" : 2
}

A4_SIZE = {"w":8.47, "h":11.67}
A4_SIZE_TURN = {"w":11.67, "h":8.47}

class graph_base():
    @staticmethod
    def set_color_counter_zero():
        graph_base.__color_counter = 0
    
    @staticmethod
    def set_color_num(color_num_max):
        graph_base.__color_num = color_num_max

    @staticmethod
    def get_color_counter():
        num = graph_base.__color_counter 
        graph_base.__color_counter +=1
        if num >= graph_base.__color_num:
            graph_base.set_color_counter_zero()
            num = graph_base.__color_counter 
        return num

    def __init__(self, width=A4_SIZE_TURN["w"], height=A4_SIZE_TURN["h"], bpi=100, second_y_ax=False): # cm, dpi
        self.fig, self.ax1 = plt.subplots(figsize=(width,height), dpi=bpi)
        self.is_second_y_ax = second_y_ax
        if second_y_ax:
            self.ax2 = self.ax1.twinx()


    def set_color_variation(self, key_num):
        self.colors = []
        for i in range(key_num):
            if i < len(BASE_COLORS):
                self.colors.append(BASE_COLORS[i])
            else:
                color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
                self.colors.append(color)
        graph_base.set_color_num(key_num)


    def set_monthly_tics(self, ax, main_priod=6, sub_priod=1):
        ax.set_xlim([FIRST_DAY, TODAY])
        ax.xaxis.set_major_formatter(mdates.DateFormatter(DATE_PATARN))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=main_priod))
        ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=sub_priod))
        self.fig.autofmt_xdate()


    def set_text_box(self, text, pos_x=0, pos_y=0, font_size=10):
        self.ax1.text(pos_x, pos_y, text, fontsize=font_size, bbox=TEXT_BOX_STYLE)


    def save_figure(self, path, title, x_label, y1_label, y2_label=""):
        today_str = datetime.today().strftime(DATE_PATARN)
        # Common
        self.ax1.set_title( title + " " + today_str)
        self.fig.legend()
        # Label
        self.ax1.set_xlabel(x_label)
        self.ax1.set_ylabel(y1_label)
        if self.is_second_y_ax:
            self.ax2.set_ylabel(y2_label)

        self.fig.savefig(path)
        print("====", os.path.basename(path) ,"===")


    # === For axis ===
    def set_ax_textbox(self, ax, text, pos_x=0, pos_y=0, font_size=10):
        ax.text(pos_x, pos_y, text, fontsize=font_size, bbox=TEXT_BOX_STYLE)

    def set_ax_monthly_tics(self, ax, main_priod=6, sub_priod=1):
        ax.xaxis.set_major_formatter(mdates.DateFormatter(DATE_PATARN))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=main_priod))
        ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=sub_priod))

    def axis_ticks_color_white(self, ax):
        ax.tick_params(axis='x', color='#FFFFFF')


class multi_graph(graph_base):
    plot_area_h=A4_SIZE_TURN["h"]/3
    plot_area_w=A4_SIZE_TURN["w"]

    def __init__(self, graph_num, col_num=1, dpi=100, second_y_ax=False):
        self.set_color_variation(5)
        self.row_num = int(graph_num/ col_num)
        self.col_num = col_num
        self.graph_num = self.row_num * self.col_num
        self.is_second_y_ax = second_y_ax

        self.plot_area_w /= col_num
        self.fig = plt.figure(figsize = (self.plot_area_w*self.col_num,
                                        self.plot_area_h*self.row_num)
                                        ,dpi=dpi)
        self.fig.autofmt_xdate()
        plt.subplots_adjust(wspace=0.4, hspace=.6)
        
        self.ax_list = []
        for row in range(self.row_num):
            for col in range(self.col_num):
                self.ax_list.append(self.fig.add_subplot(self.graph_num, col+1, row+1)) #(Total num, col, row)
                self.set_ax_monthly_tics(self.ax_list[-1])

            #if row < self.row_num-1:
            #    self.axis_ticks_color_white(self.ax_list[-1])
        

    def save_figure(self, path, title):
        create_new_dir(os.path.dirname(path))
        today_str = datetime.today().strftime(DATE_PATARN)
        self.ax_list[0].set_title( title + " " + today_str)
        #self.fig.legend()

        self.fig.savefig(path)
        print("====", os.path.basename(path) ,"===")
