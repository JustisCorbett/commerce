from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=64)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image = models.URLField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True)

class Bid(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()

class Comment(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()

class Watch(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )