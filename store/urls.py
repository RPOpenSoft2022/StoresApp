from django.urls import path
from . import views

urlpatterns = [
    path('stores/', views.storeList),
    path('stores/<int:pk>', views.storeDetail),
    path('items/',views.itemList),
    path('items/<int:pk>/',views.itemDetail),
    path('searchStorewithItem/',views.storeItem),
    path('addMenuItem/',views.addMenuItem),
    path('itemRate/',views.itemRating),
    path('updateQuantity/',views.updateQuantity),
    path('verify_order/',views.validationQuantity),
    path('order_summary/', views.orderSummary),
    path('store_manager/',views.store_manager)
    ]


#[{itemid,storeid,quantity}], [{item:{itemid,quantity},storeid}]