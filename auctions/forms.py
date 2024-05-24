
from django import forms
from .models import Listing
from django.forms import ModelForm

class BidForm(forms.Form):
    bid_amount = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)

    def clean_bid_amount(self):
        bid_amount = self.cleaned_data['bid_amount']
        return bid_amount



class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields= ["title", "description", "image"]
