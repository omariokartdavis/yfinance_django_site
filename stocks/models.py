from django.db import models
from simple_history.models import HistoricalRecords
from django.urls import reverse
import yfinance as yf
import datetime as dt

# Create your models here.

class Stock(models.Model):
    """A model to hold stock info."""
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['name', '-date_created']
        
    def __str__(self):
        """String for representing the model object."""
        return self.ticker
    
    def get_absolute_url(self):
        return reverse('stock_detail', args=[str(self.id)])
    
    def update_price(self):
        '''update the stocks price'''
        ticker = self.ticker
        
        stock = yf.Ticker(ticker)
        history = stock.history(period='1d', interval='1m')
        
        if not history.empty:
            price = Price.objects.get(stock=self)
            for i in range(0, len(history['Close'])):
                timestamp = str(history['Close'].index[i])
                datetime_of_timestamp = dt.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S%z')
                if price.time_stock_was_read and datetime_of_timestamp <= price.time_stock_was_read:
                    continue
                else:
                    price_at_datetime = history['Close'][i]
                    price.stock_price = price_at_datetime
                    price.time_stock_was_read = datetime_of_timestamp
                    price.save()
    
    def add_new_stock(self):
        """adding a new stock with last 2 days of price data to the database"""
        ticker=self.ticker
        
        stock = yf.Ticker(ticker)
        history = stock.history(period='2d', interval='1m')
        
        if not history.empty:
            self.name = stock.info['longName']
            self.save()
            
            if not Price.objects.filter(stock=self).exists():
                new_price = Price(stock=self)
            else:
                new_price = Price.objects.get(stock=self)
            for i in range(0, len(history['Close'])):
                timestamp = str(history['Close'].index[i])
                datetime_of_timestamp = dt.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S%z')
                if new_price.time_stock_was_read and datetime_of_timestamp <= new_price.time_stock_was_read:
                    continue
                
#                if not Price.objects.filter(stock=self).exists():
#                    new_price = Price(stock=self, stock_price = price_at_datetime, time_stock_was_read=datetime_of_timestamp)
#                    new_price.save()
#                else:
#                    price = Price.objects.get(stock=self)
                else:
                    price_at_datetime = history['Close'][i]
                    new_price.stock_price = price_at_datetime
                    new_price.time_stock_was_read = datetime_of_timestamp
                    new_price.save()
        else:
            #note that if I change the standard delete method of the model, calling this delete here WILL NOT call my changes to the delete method. google model delete to figure out how to delete and include special delete methods if necessary
            self.delete()
	
class Price(models.Model):
    """A model designed to hold price information for a stock."""
    
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE)
    time_stock_was_read = models.DateTimeField(blank=True, null=True)
    stock_price = models.DecimalField(max_digits=15, decimal_places=5)
    
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-time_stock_was_read']
        
    def __str__(self):
        return str(self.stock_price)