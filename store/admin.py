from django.contrib import admin
from .models import Store, StoreRating, Item, StoreMenu

# Register your models here.
admin.site.register(Store)
admin.site.register(StoreRating)
admin.site.register(Item)
admin.site.register(StoreMenu)