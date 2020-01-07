from django.contrib import admin
from stocks.models import Stock, Price

class PriceInline(admin.StackedInline):
	model = Price
	extra = 0
	
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
	inlines = [PriceInline]
	list_display = ('ticker', 'name', 'date_created')
	
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
	list_display = ('stock_price', 'stock', 'time_stock_was_read')