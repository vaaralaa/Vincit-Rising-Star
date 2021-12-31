#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 16:51:21 2021

@author: Antti
"""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date, timedelta
from tkcalendar import DateEntry
from vincit_functions import date_to_timestamp, get_data, downward, plot,\
max_volume, max_profit

# Help
today = date.today()
week_before = today - timedelta(7)
time = datetime.min.time()

window = tk.Tk()
window.title('Vincit Rising Star')
window.geometry("450x350")
window.columnconfigure(0,weight=1)
window.columnconfigure(1,weight=1)



ids = ['bitcoin','ethereum']
vs_currencies = ['eur']

# Currency id, dropdown menu
c_id_label = tk.Label(text="Currency:")
c_id_label.grid(column=0,row=0,sticky = tk.W)
c_id = tk.StringVar(window)
c_id.set(ids[0]) # default value
c_id_menu = tk.OptionMenu(window, c_id, *ids)
c_id_menu.grid(column=1,row=0,sticky = tk.EW)

# VS currency, dropdown menu
vs_c_label = tk.Label(text="VS Currency:")
vs_c_label.grid(column=0,row=1,sticky = tk.W)
vs_c = tk.StringVar(window)
vs_c.set(vs_currencies[0]) # default value
vs_c_menu = tk.OptionMenu(window, vs_c, *vs_currencies)
vs_c_menu.grid(column=1,row=1,sticky = tk.EW)

# Date from, DateEntry
df_label = tk.Label(text="From:")
df_label.grid(column=0,row=2,sticky = tk.W)
df = DateEntry(window, locale='en_FI', selectmode = 'day',
               year = week_before.year, month = week_before.month,
               day = week_before.day)
df.grid(column=1,row=2,sticky = tk.EW)

# Date to, DateEntry
dt_label = tk.Label(text="To:")
dt_label.grid(column=0,row=3,sticky = tk.W)
dt = DateEntry(window, locale='en_FI', selectmode = 'day',
               year = today.year, month = today.month,
               day = today.day)
dt.grid(column=1,row=3,sticky = tk.EW)


reset_button = tk.Button(text="reset")
reset_button.grid(column=1,row=4,sticky = tk.W)

submit_button = tk.Button(text="submit")
submit_button.grid(column=1,row=4,sticky = tk.E)

# Downward trend
dw_label = tk.Label(text="Longest downward trend:")
dw_label.grid(column=0,row=5,sticky = tk.W)
dw = tk.Text(window, state='disabled',height=3)
dw.grid(column=0,row=6,columnspan = 2)

# Highest trading volume
hv_label = tk.Label(
        text="Day with highest trading volumes and amount in euros:")
hv_label.grid(column=0,row=7,columnspan=2,sticky = tk.W)
hv = tk.Text(window, state='disabled',height=2)
hv.grid(column=0,row=8,columnspan = 2)

# Max profit
mp_label = tk.Label(
        text="Best date to buy and sell and maximum profit in euros:")
mp_label.grid(column=0,row=9,columnspan=2,sticky = tk.W)
mp = tk.Text(window, state='disabled',height=4)
mp.grid(column=0,row=10,columnspan = 2)


def submit(event):
    """
    Gets the data, processes it and displays processed data on main window and
    graph on new window
    """
    # get parameters from user
    id_val = c_id.get()
    vs_val = vs_c.get()
    f = date_to_timestamp(df.get_date(), time)
    t = date_to_timestamp(dt.get_date(), time)
    if f > t:
        messagebox.showerror("Date range error",
                             "From must be earlier date than To!")
    else:
        # get data from CoinGeckoAPI
        data, date_range = get_data(id_val,vs_val,f,t)
        
        # get longest downward trend and display results in window
        down = downward(data[:,0],len(date_range))
        dw_text = ""
        if down[1] > 0:
            dw_text = "In {}’s historical data from CoinGecko,\
the price decreased {} days in a row for the inputs from {} to {}.".format(
id_val,down[1],date_range[down[0]].strftime("%Y-%m-%d"),
                          date_range[down[0]+down[1]].strftime("%Y-%m-%d"))      
        else:
            dw_text = "In bitcoin’s historical data from CoinGecko,\
the price decreased {} days in a row.".format(down[1])

        dw.config(state='normal')
        dw.delete(1.0,tk.END)
        dw.insert(tk.END,dw_text)
        dw.config(state='disabled')
        
        highest_volume = max_volume(data[:,1],date_range)
        hv_text = "Day with highest trading volume within date range is {} and\
amount in euros {}€.".format(highest_volume[0].strftime("%Y-%m-%d"),
        highest_volume[1])
        hv.config(state='normal')
        hv.delete(1.0,tk.END)
        hv.insert(tk.END,hv_text)
        hv.config(state='disabled')
        
        pair, profit = max_profit(data[:,0],date_range)
        if profit != -1:
            mp_text = "To get maximum profit from buying and selling, the best\
 date to buy is {} and the best day to sell is {} \
and the amount of profit is {}€ from one coin.".format(
date_range[pair[0]].strftime("%Y-%m-%d"),
date_range[pair[1]].strftime("%Y-%m-%d"),profit)
        else:
            mp_text = "No possible profit, within the chosen date range one \
shouldn\'t buy nor sell."
        mp.config(state='normal')
        mp.delete(1.0,tk.END)
        mp.insert(tk.END,mp_text)
        mp.config(state='disabled')
        
        new_window = tk.Toplevel(window)
        new_window.title("Visual representation of the data")
        plot(new_window, data[:,0], down,date_range,pair)

def reset(event):
    """
    resets window's values
    """
    c_id.set(ids[0])
    vs_c.set(vs_currencies[0])
    df.set_date(week_before)
    dt.set_date(today)
    dw.config(state='normal')
    dw.delete(1.0,tk.END)
    dw.config(state='disabled')
    hv.config(state='normal')
    hv.delete(1.0,tk.END)
    hv.config(state='disabled')
    mp.config(state='normal')
    mp.delete(1.0,tk.END)
    mp.config(state='disabled')

reset_button.bind("<Button-1>", reset)
submit_button.bind("<Button-1>", submit)

window.mainloop()