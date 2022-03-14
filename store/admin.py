from django.contrib import admin
from .models import Store, StoreRating, items, StoreMenu

# Register your models here.
admin.site.register(Store)
admin.site.register(StoreRating)
admin.site.register(items)
admin.site.register(StoreMenu)