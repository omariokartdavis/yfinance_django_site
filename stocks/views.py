from django.shortcuts import render

from stocks.models import Stock, Price

def index(request):
	"""View function for home page of site."""
	
	num_stocks = Stock.objects.all().count()
	
	recent_5_stocks_added = Stock.objects.order_by('-date_created')[:5]
	
	context = {
		'num_stocks' : num_stocks,
		'recent_5_stocks_added' : recent_5_stocks_added,
	}
	
	return render(request, 'index.html', context=context)