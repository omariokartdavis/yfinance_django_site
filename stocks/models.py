from django.db import models

# Create your models here.

class Stock(models.Model):
	"""A model to hold stock info."""
	ticker = models.CharField(max_length=10)
	name = models.CharField(max_length=100)
	date_created = models.DateTimeField(auto_now_add = True)
	
	def __str__(self):
		"""String for representing the model object."""
		return self.ticker
	
class Price(models.Model):
	"""A model designed to hold price information for a stock."""
	
	stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	stock_price = models.DecimalField(max_digits=15, decimal_places=5)
	
	class Meta:
		ordering = ['-date']
		
	def __str__(self):
		return str(self.stock_price)