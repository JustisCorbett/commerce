from django import forms
from django.db.models import Max

from .models import Category, Listing, Bid, Comment


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["category", "title", "description", "starting_bid", "image"]
        labels = {
            "starting_bid": "Starting Bid (to the nearest dollar)",
            "category": "Category",
            "title": "Listing Title",
            "description": "Description",
            "image": "Image URL",
        }
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "starting_bid": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.URLInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "title": {
                "required": "Please enter a title.",
            },
            "category": {
                "required": "Please select a category.",
            },
            "description": {
                "required": "Please enter a description.",
            },
            "starting_bid": {
                "required": "Please enter a starting bid(to the nearest dollar).",
            },
        }

class BidForm(forms.ModelForm):
    # add field "title" that is not in the model in order to validate amount
    title = forms.CharField()
    class Meta:
        model = Bid
        fields = ["amount", "title"]
        labels = {"amount": "Bid amount (to the nearest dollar)"}
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }
        error_messages = {"amount": {
            "required": "Please enter a valid bid.",
        }}

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        title = self.data["title"]
        #Check if listing has bids. If it doesnt, use the listings starting_bid to validate
        bids = Bid.objects.filter(listing__title=title)
        if not bids:
            listing = Listing.objects.get(title=title)
            highest_bid = listing.starting_bid
        else:
            highest_bid = bids.aggregate(Max("amount"))
        if amount <= highest_bid["amount__max"]:
            raise forms.ValidationError("Bid must be more than current highest bid.")
        return amount

    #def __init__(self, *args, **kwargs):
    #    self.title = kwargs.pop("title")
    #    super(BidForm, self).__init__(*args, **kwargs)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]