from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer

############# Creating API View : 00:15:07 ##############
############# Serializing Objects: 00:28:08 #############
############ Deserializing Objects : 00:52:37 #############
############ Data Validation : 00:55:14 #############
############# Class Based Views: 01:18:20 ############

# -----------------------------------------------------------------------------------------------
# Function Based Views 

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)

#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('ok')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         serializer.validated_data
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     # try:
#     #     product = Product.objects.get(pk=id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)
#     # except Product.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.order_items.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products'))
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(('GET', 'PUT', 'DELETE'))
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(
#             products_count=Count('products')),  # products is defined in the related fields in the ollection attribute of Product model
#             pk=pk)      
#     if request.method == 'GET':
#         serializer=CollectionSerializer(collection, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED) 
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error': 'Colelction cannot be deleted because it includes one or more products.'}, \
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
# Class Based Views 

class ProductList(APIView):
    def get(self,request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)  
    
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.order_items.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
