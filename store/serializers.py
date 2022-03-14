from rest_framework import serializers
from .models import Store, StoreRating, items, StoreMenu

class StoreSerializer(serializers.ModelSerializer):
    menu = serializers.PrimaryKeyRelatedField(queryset=items.objects.all(), many=True)
    class Meta:
        model = Store
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    stores = StoreSerializer(many=True, read_only=True)
    class Meta:
        model = items
        fields='__all__'


class StoreRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRating
        fields = '__all__'

class StoreMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=StoreMenu
        fields='__all__'