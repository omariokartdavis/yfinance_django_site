from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from stocks.models import Stock
from stocks.forms import AddNewStockForm

def index(request):
    """View function for home page of site."""
    
    if request.method == 'POST':
        if 'add new stock' in request.POST:
            form = AddNewStockForm(request.POST)
            if form.is_valid():
                stock_ticker = form.cleaned_data['ticker'].upper()
                if not Stock.objects.filter(ticker=stock_ticker):
                    new_stock = Stock(ticker=stock_ticker)
                    new_stock.save()
                else:
                    new_stock = Stock.objects.get(ticker=stock_ticker)
                new_stock.add_new_stock()
            
            return HttpResponseRedirect(reverse('index'))
            
    num_stocks = Stock.objects.all().count()
    new_stock_form = AddNewStockForm()    
    all_stocks = Stock.objects.all()
    
    context = {
        'num_stocks' : num_stocks,
        'all_stocks': all_stocks,
        'new_stock_form': new_stock_form,
    }
    
    return render(request, 'index.html', context=context)

def stock_detail(request, pk):
    """View an individual Stocks info"""
    stock = Stock.objects.get(id=pk)
    
    context= {
        'stock' : stock,
        }
    
    return render(request, 'stocks/stock_detail.html', context=context)

def delete_stock(request, pk):
    """Delete stock, likely for if an incorrect ticker was added"""
    
    stock = Stock.objects.get(id=pk)
    
    if request.method=="POST":
        if 'delete stock' in request.POST:
            stock.delete()
        return HttpResponseRedirect(reverse('index'))
    
    context = {
        'stock' : stock,
        }
    
    return render(request, 'stocks/delete_stock.html', context=context)