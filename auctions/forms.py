from django import forms

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]