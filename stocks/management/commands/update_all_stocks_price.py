from django.core.management.base import BaseCommand
from stocks.models import Stock
#from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Updates the price of all stocks in the database'
    
    def handle(self, *args, **kwargs):
        for i in Stock.objects.all().iterator():
            i.update_price()