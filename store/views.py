from unicodedata import name
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import StoreSerializer, StoreRatingsSerializer, ItemsSerializer, StoreMenuSerializer
from .models import Store, StoreRating, items, StoreMenu
from decimal import Decimal



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


