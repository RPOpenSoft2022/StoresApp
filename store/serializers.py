from rest_framework import serializers
from .models import Store, StoreRating, Item, StoreMenu, ItemRate

class StoreSerializer(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), many=True)
    class Meta:
        model = Store
        fields = '__all__'
    
    def to_representation(self, instance):
        menu = []
        for item in instance.menu.all():
            menu.append({"id": item.id,"name": item.name, "isVeg": item.IsVeg, "price": item.price, "thumbnail": item.thumbnail, "itemRating": item.itemRating, "itemRatingCount": item.itemRatingCount})
        return {
            "id": instance.id,
            "menu": menu,
            "locLatitude": instance.locLatitude,
            "locLongitude": instance.locLongitude,
            "address": instance.address,
            "name": instance.name,
            "availabilityTime": instance.availabilityTime,
            "rating": instance.rating,
            "ratingCount": instance.ratingCount,
            "contactInfo": instance.contactInfo
        }


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields='__all__'


class StoreRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRating
        fields = '__all__'

class StoreMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=StoreMenu
        fields='__all__'

class ItemRateSerializer(serializers.ModelSerializer):
    class Meta:
        model=ItemRate
        fields='__all__'