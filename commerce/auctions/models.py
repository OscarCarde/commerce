from django.contrib.auth.models import AbstractUser
from django.db import models
import PIL

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank = True, related_name = 'watchers')
    pass


class Listing(models.Model):
    item = models.CharField(max_length = 30)
    description  = models.CharField(max_length = 250)
    created = models.DateTimeField(auto_now = True)
    price = models.DecimalField(max_digits = 11, decimal_places = 2)
    seller = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "items")
    image = models.ImageField(upload_to = 'media/photos')

    def __str__(self):
        return f"{self.item}, listed by {self.seller} on {self.created} for {self.price}"


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

    def __str__(self):
        return f"{self.commenter} posted on {self.posted}: {self.comment}"
