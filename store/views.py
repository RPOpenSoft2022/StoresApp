from functools import partial
from unicodedata import name
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import StoreSerializer, StoreRatingsSerializer, ItemsSerializer, StoreMenuSerializer, ItemRateSerializer
from .models import Store, StoreRating, Item, StoreMenu
from decimal import Decimal
from django.http import JsonResponse
import json
from .interconnect import send_request_post, send_request_get
from rest_framework.exceptions import ValidationError
from store_ms.settings import DELIVERY_MICROSERVICE_URL, STORES_MICROSERVICE_URL, USERS_MICROSERVICE_URL, SECRET_KEY
import jwt
from corsheaders.defaults import default_headers
import requests

from store import serializers
# Create your views here.
@api_view([ 'GET', 'POST'])
def storeList(request):
    if request.method == 'POST':
        print(request.data)
        serializer = StoreSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Successful"}, status=status.HTTP_200_OK)

        return Response({"msg": "Failure", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # loc_lat = request.GET['locLatitude']
        # loc_long = request.GET['locLongitude']
        stores = list(Store.objects.all())
        # stores = sorted(stores, key=lambda store: abs(store.locLatitude - Decimal(loc_lat)) +
        #                                           abs(store.locLongitude - Decimal(loc_long)))
        serializer = StoreSerializer(stores, many=True)
        return Response({"stores": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def storeDetail(request, pk):
    if request.method == 'GET':
        store = Store.objects.get(id=pk)
        serializer = StoreSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        store = Store.objects.get(id=pk)
        serializer = StoreSerializer(store, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        store = get_object_or_404(Store, id=pk)
        store.delete()
        return Response({"msg": "Successful"}, status=status.HTTP_200_OK)

    return Response({"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def itemList(request):
    if request.method == 'GET':
        item = Item.objects.all()
        serializer = ItemsSerializer(item,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ItemsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"messages":"Successful"},status=status.HTTP_201_CREATED)

        return Response({"msg":"Failure","error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def itemDetail(request,pk):

    if request.method == 'GET':
        item = Item.objects.get(id=pk)
        serializer = ItemsSerializer(item,many=False)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        item = Item.objects.get(id=pk)
        item.delete()
        return Response({"messages": "Successful"},status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        item = Item.objects.get(id=pk)
        print(item.ratingCount)
        serializer = ItemsSerializer(instance=item,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"messages": "Successful"},status=status.HTTP_200_OK)
        else:
            print(serializer.error_messages)
            return Response({"messages": "Failure"},status=status.HTTP_400_BAD_REQUEST)
def validation(str):
    str=str.strip()
    str=str.lower()
    return str

@api_view(['POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def storeRate(request):
    if request.method == 'POST':
        serializer = StoreRatingsSerializer(data=request.data)

        if serializer.is_valid():
            store = serializer.validated_data['storeId']
            store.rating = (store.rating * store.ratingCount + serializer.validated_data['rating']) / \
                           (store.ratingCount + 1)
            store.ratingCount += 1
            store.save()
            serializer.save()
            return Response({"msg": "Successful"}, status=status.HTTP_200_OK)

        return Response({"msg": "Failure", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def storeItem(request):
    foodName = validation(request.GET['itemName'])
    item = Item.objects.get(name=foodName)
    storeItem = item.stores.all()
    serializer = StoreSerializer(storeItem,many=True)
    storeitem = []

    for i in serializer.data:
        storeitem.append(i['name'])

    return Response(storeitem,status=status.HTTP_200_OK)

    
        

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def addMenuItem(request):
    if request.method == 'POST':
        serializer=StoreMenuSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"messages":"Successful"},status=status.HTTP_201_CREATED)

        return Response({"msg":"Failure","error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        storeMenu = StoreMenu.objects.all()
        serializer=StoreMenuSerializer(storeMenu ,many=True)
        return Response(serializer.data)


@api_view(['POST'])
def itemRating(request):
    serializer = ItemRateSerializer(data=request.data)

    if serializer.is_valid():
        it = serializer.validated_data['itemId']
        it.itemRating = (it.itemRating * it.itemRatingCount + serializer.validated_data['rating']) / \
                        (it.itemRatingCount + 1)
        it.itemRatingCount += 1
        it.save()
        serializer.save()
        return Response({"msg": "Successful"}, status=status.HTTP_200_OK)

    return Response({"msg": "Failure", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def convert(b):
    
    c=[]
    # X_list=json.loads(b['item_list'][0]),
    X_list = b['item_list']
    print(X_list)
    # print(json.loads(X_list[0]))
    for i in X_list:
        #print(X_list[i][0].get('item_id'))
        # for j in range(len(X_list[i])):            
        dict1={
            
            "item":i['id'],
            "store":b['store_id'],
            "quantity":i['quantity']
        }
        c.append(dict1)
    
    return c
@api_view(['POST'])
def validationQuantity(request):
    serializer =StoreMenuSerializer(data=convert(request.data),many=True)
    
   # print(convert(request.data))
    if serializer.is_valid():
        for data in serializer.validated_data:
            storeMenu=StoreMenu.objects.get(store=data['store'],item=data['item'])
            if storeMenu.quantity-data['quantity'] < 0:
                return Response({"msg":'false'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":'true', "store_name":storeMenu.store.name},status=status.HTTP_200_OK)    
    return Response({"msg": "Failure", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateQuantity(request):
    serializer =StoreMenuSerializer(data=convert(request.data),many=True)
    
    #print(convert(request.data))
    if serializer.is_valid():
        for data in serializer.validated_data:
            storeMenu=StoreMenu.objects.get(store=data['store'],item=data['item'])
            storeMenu.quantity-=data['quantity']
            if storeMenu.quantity < 0:
                return Response({"msg": "not enough quantity"}, status=status.HTTP_400_BAD_REQUEST)
            print(storeMenu)
            storeMenu.save()
        return Response({"msg": "Successful"}, status=status.HTTP_200_OK)
    return Response({"msg": "Failure", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def orderSummary(request):
    print(30*'-')
    print(request.data['item_list'])
    print(30*'-')
    items = request.data['item_list']
    cost = 0
    for item in items:
        obj = Item.objects.get(id=item["id"])
        item['name'] = obj.name
        item['price'] = obj.price
        cost += obj.price * item["quantity"]
    return JsonResponse({"item_list": items, "total_cost": cost})

@api_view(['POST'])
def store_manager(request):
    store = Store.objects.get(ownerId=request.data['user_id'])
    serializer = StoreSerializer(store)
    return Response(serializer.data,status=status.HTTP_200_OK)
