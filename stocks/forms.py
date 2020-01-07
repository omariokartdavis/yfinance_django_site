from django import forms

class AddNewStockForm(forms.Form):
    ticker = forms.CharField(max_length=10)