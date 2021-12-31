#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 18:55:02 2021

@author: Antti
"""
from pycoingecko import CoinGeckoAPI
import numpy as np
from datetime import datetime, timedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

def date_to_timestamp(date, time):
    """
    Takes in date and time and returns given date as a timestamp
    """
    return int(datetime.timestamp(datetime.combine(date, time)))

def get_data(c_id,vs_c,df,dt):
    """
    Takes in c_id as currency id, vs_c as vs currency, df as timestamp of
    from date and dt as timestamp of to date. Gets data from CoinGeckoAPI()
    and returns chosen_data as [days_price,total_volumes] and date_range.
    days_price, total_volumes and date_range all corresponds to certain day
    with same id
    """
    cg = CoinGeckoAPI()
    # add 1 hour to dt to make sure to get the right price for the last day
    data = cg.get_coin_market_chart_range_by_id(c_id,vs_c, df, dt + 3600)
    prices = np.array(data["prices"])
    dates = prices[:,0]
    prices = prices[:,1]
    total_volumes = np.array(data["total_volumes"])[:,1]
    start = datetime.fromtimestamp(df).date()
    end = datetime.fromtimestamp(dt).date()
    date_range = np.arange(start, end+timedelta(1),
                           timedelta(days=1)).astype(datetime)
    nr_of_days = len(date_range)
    chosen_data = np.zeros((nr_of_days,2))
    
    for i in range(nr_of_days):
        id_nearest = np.abs(dates/1000 - ((df+i*86400))).argmin()
        chosen_data[i] = [prices[id_nearest],total_volumes[id_nearest]]
    
    return chosen_data, date_range

def downward(days_price, nr_of_days):
    """
    Takes in day's prices and number of days, returns the longest downward 
    streak as pair of id of start point and streak length
    """
    start = 0 # start point
    streak = 0 # streak length
    longest_streak = [0,0] # start point and streak length
    prev = 0
    for i in range(nr_of_days):
        if prev != 0:
            if days_price[i]<prev:
                streak +=1
                if i == nr_of_days-1 and longest_streak[1] < streak:
                    longest_streak = [start,streak]
            else:
                if longest_streak[1] < streak:
                    longest_streak = [start,streak]
                streak = 0
                start = i
        prev = days_price[i]
    
    
    
    return longest_streak

def plot(window,days_price,longest_streak,date_range,pair):
    """
    Takes in window where to draw the graph, data as day's prices, longest
    downward streak, date range and pair of buy and sell dates for max profit,
    draws graph of days_price, longest downward streak and the best date to
    sell and buy on given window
    """
    # select downward streak from days_price
    down = days_price[longest_streak[0]:longest_streak[0]+longest_streak[1]+1]
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)
    
    
    # add subplot
    plot1 = fig.add_subplot(111)
    # plot days_price and down
    plot1.plot(date_range,days_price)
    plot1.plot(date_range[longest_streak[0]:longest_streak[0]+
                          longest_streak[1]+1],down, '--r')
    # scatter plot best date to buy and sell
    if pair != [-1,-1]:
        plot1.scatter(date_range[pair[0]],days_price[pair[0]],
                      marker='x', c='green')
        plot1.scatter(date_range[pair[1]],days_price[pair[1]],
                      marker='x', c='black')
    
    plot1.legend(('Day\'s price','Downward','Buy','Sell'))
    plot1.tick_params(labelrotation=30)
  
    # create canvas containing the figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


def max_volume(trading_volumes, date_range):
    """
    Takes in trading volumes as data, date_range and returns max_volume as date
    and amount in euros
    """
    max_volume = [0,0]
    max_id = trading_volumes.argmax()
    max_volume = [date_range[max_id],trading_volumes[max_id]]
    return max_volume


def max_profit(days_price,date_range):
    """
    Takes in data as day's price and date range, return pair of days and
    max profit in euros, if there's no profit to be made, returns pair of -1's 
    and -1 profit
    """
    
    nr_of_days = len(date_range)
    buy_sell_pairs = []
    profits = []
    i = 0


    while i < nr_of_days-1:
        # Finds first local min
        while i < nr_of_days-1 and days_price[i] > days_price[i+1]:
            i += 1
        if i == nr_of_days-1:
            break
        local_min = i
        # find id for maximum value from days_price after local min
        sell = local_min + np.array(days_price[local_min:]).argmax()
        # find id for minimum value between local min and max value
        buy = local_min + np.array(days_price[local_min:sell+1]).argmin()

        buy_sell_pairs.append([buy,sell])
        i = sell+1
    
    if buy_sell_pairs == []:
        return [-1,-1],-1
    for pair in buy_sell_pairs:
        profits.append(days_price[pair[1]]-days_price[pair[0]])
    # finds id for max profit so max profit pair can be returned
    max_profit_id = np.argmax(profits)
    return (buy_sell_pairs[max_profit_id],profits[max_profit_id])
