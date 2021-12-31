# Vincit-Rising-Star
Author: Antti Vaarala
Coded on macOS 10.15.2
python 3.6.4
Packages and installing
tkinter - pip install tk
DateTime - pip install DateTime
tkcalendar - pip install tkcalendar
pycoingecko - pip install pycoingecko
matplotlib - pip install matplotlib
NumPy - pip install numpy

Running program (mac terminal):
git clone https://github.com/vaaralaa/Vincit-Rising-Star.git
cd Vincit-Rising-Star
python3 Vincit.py

Vincit.py is the main program, that asks parameters from user to get bitcoin rate in euros. (can be easily modified to support more coins and currencies than bitcoin and euro). Reset button resets the window to default settings, when submit is pressed, submit function calls functions from vincit_fucntions.py that process and display the data in main window and graph in new window.

Functions in Vincit.py
submit(event):
    Gets the data, processes it and displays processed data on main window and
    graph on new window

reset(event):
    resets window's values
    

Functions in vincit_functions.py
date_to_timestamp(date, time):
    Takes in date and time and returns given date as a timestamp

get_data(c_id,vs_c,df,dt):
    Takes in c_id as currency id, vs_c as vs currency, df as timestamp of
    from date and dt as timestamp of to date. Gets data from CoinGeckoAPI()
    and returns chosen_data as [days_price,total_volumes] and date_range.
    days_price, total_volumes and date_range all corresponds to certain day
    with same id

downward(days_price, nr_of_days):
    Takes in day's prices and number of days, returns the longest downward 
    streak as pair of id of start point and streak length

plot(window,days_price,longest_streak,date_range,pair):
    Takes in window where to draw the graph, data as day's prices, longest
    downward streak, date range and pair of buy and sell dates for max profit,
    draws graph of days_price, longest downward streak and the best date to
    sell and buy on given window

max_volume(trading_volumes, date_range):
    Takes in trading volumes as data, date_range and returns max_volume as date
    and amount in euros

max_profit(days_price,date_range):
    Takes in data as day's price and date range, return pair of days and
    max profit in euros, if there's no profit to be made, returns pair of -1's 
    and -1 profit