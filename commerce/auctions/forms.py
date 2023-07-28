from django.forms import ModelForm, TextInput, Textarea
from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item', 'description', 'price', 'image']
        exclude = ['seller']
        widgets = {
            "item": TextInput(attrs={'class': ''}),
            "description": Textarea(attrs={'class':'my-5'})
        }
        labels= {
            "item": "Title",
            "description": "'Enter your item\'s description here'",
            "price": 'Price'
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        exclude = ['bider', 'item']