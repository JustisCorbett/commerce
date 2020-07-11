from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    title = models.CharField(max_length=64)

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image = models.URLField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
    )

class Bids(models.Model):
    listing = models.ForeignKey(
        Listings,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()

class Comments(models.Model):
    listing = models.ForeignKey(
        Listings,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()

