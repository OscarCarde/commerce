from django.forms import ModelForm, TextInput, Textarea
from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item', 'description', 'price', 'image', 'category']
        exclude = ['seller', 'winner']
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
        labels = {
            'bid': 'place your bid'
        }

class CommentForm(ModelForm):
    class Meta:
        model= Comment
        fields= ['comment']
        widgets = {
            'comment': Textarea(attrs={'id': 'comment-textarea', 'class':'form-control', 'placeholder': "Comment here"})
        }