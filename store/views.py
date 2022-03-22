from unicodedata import name
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import StoreSerializer, StoreRatingsSerializer, ItemsSerializer, StoreMenuSerializer, ItemRateSerializer
from .models import Store, StoreRating, items, StoreMenu
from decimal import Decimal
from django.http import JsonResponse
import json


# Create your views here.
@api_view([ 'GET', 'POST'])
def storeList(request):
    if request.method == 'POST':
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
        serializer = StoreSerializer(store, data=request.data)

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
        item=items.objects.all()
        serializer=ItemsSerializer(item,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer=ItemsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"messages":"Successful"},status=status.HTTP_201_CREATED)

        return Response({"msg":"Failure","error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def itemDetail(request,itemname):

    if request.method == 'GET':
        item=items.objects.get(name=itemname)
        serializer=ItemsSerializer(item,many=False)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        item = items.objects.get(name=itemname)
        item.delete()
        return Response({"messages":"Successful"},status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        item=items.objects.get(name=itemname)
        serializer=ItemsSerializer(instance=item,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"messages":"Successful"},status=status.HTTP_200_OK)

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
    foodName=validation(request.GET['itemName'])
    item=items.objects.get(name=foodName)
    storeItem=item.stores.all()
    serializer=StoreSerializer(storeItem,many=True)
    storeitem=[]

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
    X_list=b.get('item-list'),
    #print(X_list)
    for i in range(len(X_list)):
        #print(X_list[i][0].get('item_id'))
        for j in range(len(X_list[i])):
            
            dict1={
                
                "item":X_list[i][j].get('item_id'),
                "store":b.get('store_id'),
                "quantity":X_list[i][j].get('qty')
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
                return Response(False, status=status.HTTP_400_BAD_REQUEST)
        return Response(True,status=status.HTTP_200_OK)    
    return Response({"msg": "Failure", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateQuantity(request):
    a=validation(request.GET['cancellation'])
    
    if a=="true":
       cancel=True
    else:
        cancel=False

    serializer =StoreMenuSerializer(data=convert(request.data),many=True)
    
    #print(convert(request.data))
    if serializer.is_valid():
        for data in serializer.validated_data:
            storeMenu=StoreMenu.objects.get(store=data['store'],item=data['item'])
            if cancel is not True:
                storeMenu.quantity-=data['quantity']
                if storeMenu.quantity < 0:
                    return Response({"msg": "not enough quantity"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                storeMenu.quantity+=data['quantity']
            storeMenu.save()
        return Response({"msg": "Successful"}, status=status.HTTP_200_OK)
    return Response({"msg": "Failure", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def orderPrepared(request):
    orderId=request.data['orderId']
    storeId=request.data['storeId']
    return JsonResponse({"orderId":orderId})

