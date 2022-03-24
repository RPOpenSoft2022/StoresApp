from asyncio.windows_events import NULL
from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50)
    IsVeg = models.BooleanField(default=True)
    price = models.IntegerField()
    thumbnail = models.CharField(max_length=50)
    itemRating = models.DecimalField(max_digits=3, decimal_places=2)
    itemRatingCount = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class JSONAPIMeta:
        resource_name = 'items'


class Store(models.Model):
    # positive means North, negative means South
    locLatitude = models.DecimalField(max_digits=8, decimal_places=3)
    # positive means East, negative means West
    locLongitude = models.DecimalField(max_digits=8, decimal_places=3)
    address = models.TextField()
    name = models.CharField(max_length=50)
    availabilityTime = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    ratingCount = models.IntegerField(default=1)
    contactInfo = models.CharField(max_length=50)
    menu = models.ManyToManyField(Item, through='StoreMenu', related_name="stores")

    def __str__(self):
        return self.name


class StoreRating(models.Model):
    storeId = models.ForeignKey(Store, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)


class StoreMenu(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class ItemRate(models.Model):
    itemId = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)


    