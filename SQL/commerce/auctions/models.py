from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)
    def __str__(self):
        return self.category

class Bid(models.Model):
    new_bid = models.DecimalField(max_digits=9, decimal_places=2)
    user_bid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid", default=0)

    def __str__(self):
        return f"{self.new_bid} $"
    

class Listing(models.Model):
    product = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    minimum_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, default=0, related_name="listing_bid")
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing_category", default=None)
    isActive = models.BooleanField(default=True)
    user_watchlist = models.ManyToManyField(User, blank=True, related_name="user_watchlist", default=None)
    user_bids = models.ManyToManyField(User, blank=True, related_name="user_bids", default= None)

    def __str__(self):
        return f"{self.pk} {self.product}"
    


class Comment(models.Model):
    comment = models.CharField(max_length=250)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment", default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment", default=None)

    def __str__(self):
        return f"{self.user}: {self.comment}"
