from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank = True, related_name = 'watchers')


class Listing(models.Model):
    item = models.CharField(max_length = 30)
    description  = models.CharField(max_length = 250)
    created = models.DateTimeField(auto_now = True)
    price = models.DecimalField(max_digits = 11, decimal_places = 2)
    seller = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "items")
    image = models.ImageField(upload_to = 'media/photos', blank=True)
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name = "items_won")
    category = models.CharField(max_length = 30, blank=True)

    @property
    def max_bid(self):
        highest_bid = self.bids.aggregate(max_bid=models.Max('bid'))['max_bid']
        return highest_bid if highest_bid is not None else 0

    @property
    def bids_count(self):
        return self.bids.count()

    @property
    def comments(self):
        return self.the_comments.all()
    
    def close_auction(self):
        highest_bid = self.bids.order_by('-bid').first()
        if highest_bid:
            self.winner = highest_bid.bider
        self.save()

    @property
    def timestamp(self):
        return timesince(self.created , timezone.now()) + " ago"

    def __str__(self):
        return f"{self.item}, listed by {self.seller}, {self.timestamp} for {self.price}"


class Bid(models.Model):
    bid = models.DecimalField(max_digits = 11, decimal_places = 2)
    bider = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'bids')
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = 'bids')

    def __str__(self):
        return f"£{self.bid} from {self.bider}, for {self.item.item}, id:{self.item.id}"

class Comment(models.Model):
    comment = models.TextField(max_length = 250)
    posted = models.DateTimeField(auto_now_add = True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comments")
    listing = models.ForeignKey(Listing, blank = True, null=True, on_delete= models.CASCADE, related_name = "the_comments")

    @property
    def timestamp(self):
        return timesince(self.posted, timezone.now()) + " ago"

    def __str__(self):
        return f"{self.commenter} posted on {self.posted}: {self.comment}"