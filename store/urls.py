from django.urls import path
from . import views

urlpatterns = [
    path('stores/', views.storeList),
    path('stores/<int:pk>', views.storeDetail),
    path('items/',views.itemList),
    path('items/<str:itemname>/',views.itemDetail),
    path('searchStorewithItem/',views.storeItem),
    path('addMenuItem/',views.addMenuItem),
    path('itemRate/',views.itemRating),
    path('updateQuantity/',views.updateQuantity),
    path('validation/',views.validationQuantity)
    ]
