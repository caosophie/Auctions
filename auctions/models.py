from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class ArticleType(models.Model):
    type = models.CharField(max_length=30)
    img_type = models.URLField(default='google.com')

    def __str__(self):
        return f"{self.type}"

class ActiveListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.URLField(default='google.com')
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(ArticleType, on_delete=models.CASCADE, related_name="listing")
    categories = models.ManyToManyField(ArticleType, blank=True, related_name="listings")
    description = models.CharField(max_length=500, default="No description available")
    status = models.BooleanField(default=False)
    watching = models.CharField(max_length=50, default="Add to watchlist")

    def __str__(self):
        return f"{self.name} @ {self.bid}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} saved {self.listings}"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user} bid {self.price} on {self.listing}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    listing = models.ForeignKey(ActiveListing, on_delete=models.CASCADE, related_name="comments_listing")

    def __str__(self):
        return f"{self.comment}"