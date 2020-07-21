from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image = models.URLField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = "listings"


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

    class Meta:
        default_related_name = "bids"


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

    class Meta:
        default_related_name = "comments"


class Watch(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = "watched"
        unique_together = (('user','listing'),)
