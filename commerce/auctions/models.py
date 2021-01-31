from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import render
from django.utils.translation import ugettext as _

class User(AbstractUser):
    pass

class Listings(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=4096)
    auction_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_listings")
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=200, blank=True)
    category = models.CharField(max_length=64)
    active = models.BooleanField(default=False)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist_items")
    
    

    def __str__(self):
        return f'{self.title} by {self.auction_owner}: {self.description}: {self.starting_bid}'
    def current_bid(self):
        return max([bid.offer for bid in self.bids.all()]+[self.starting_bid])
    def winning_bidder(self):
        return self.bids.get(offer=self.current_bid()).user if self.no_of_bids() > 0 else None    
    def no_of_bids(self):
        return len(self.bids.all())

class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    offer = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_made")

    def clean(self):
        
        print(self.offer)
        print(self.listing.current_bid())
     
        if self.offer and self.listing.current_bid():
            if self.offer <= self.listing.current_bid():
                raise ValidationError({'offer': _('Your bid must be greater than the current price!')})
     

    def __str__(self):
        return f"{self.user} offers to pay ${self.offer} for the listing: {self.listing}"

class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=2048)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.commenter} made a comment to {self.listing}: {self.content}"

