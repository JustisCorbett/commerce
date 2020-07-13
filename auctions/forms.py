from django import forms
from .models import Category, Listing, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["category", "title", "description", "starting_bid", "image"]

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]