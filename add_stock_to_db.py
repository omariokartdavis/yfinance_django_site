# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 08:15:54 2020

@author: odavis
"""

# to call this function to add movements to the database run:
# python manage.py shell
# exec(open('add_stock_to_db.py').read())

import yfinance as yf
import datetime as dt
from stocks.models import Stock, Price

def add_stock_to_db(ticker):
    '''add the most recent 2 days stock history to the database at a 1 minute interval'''
    #ticker should already be in upper form from the user input
    
    stock = yf.Ticker(ticker)
    history = stock.history(period='2d', interval='1m')
    
    if not history.empty:
        if not Stock.objects.filter(ticker=ticker):
            new_stock = Stock(ticker=ticker, name=stock.info['longName'])
            new_stock.save()
        else:
            new_stock = Stock.objects.get(ticker=ticker)
        
        for i in range(0, len(history['Close'])):
            timestamp = str(history['Close'].index[i])
            datetime_of_timestamp = dt.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S%z')
            price_at_datetime = history['Close'][i]
            if not Price.objects.filter(stock=new_stock):
                new_price = Price(stock=new_stock, stock_price = price_at_datetime, time_stock_was_read=datetime_of_timestamp)
                new_price.save()
            else:
                price = Price.objects.get(stock=new_stock)
                if datetime_of_timestamp <= price.time_stock_was_read:
                    continue
                else:
                    price.stock_price = price_at_datetime
                    price.time_stock_was_read = datetime_of_timestamp
                    price.save()
                
user_inputted_ticker = str(input('Input a stock ticker such as MSFT: ')).upper()
add_stock_to_db(user_inputted_ticker)