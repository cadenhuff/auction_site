from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



    
class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField(blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_bid = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    open = models.BooleanField(default=True)
    Wishers = models.ManyToManyField(User, related_name="wishes")

    


class Bid(models.Model):
    value = models.DecimalField(decimal_places=2, max_digits = 100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bids" )

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

 

