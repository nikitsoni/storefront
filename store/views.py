from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from django.db.models.aggregates import Count


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({"error": "Cannot delete a product with associated orders"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}

# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serialise = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serialise.data)
    
#     def post(self, request):
#         serialise = ProductSerializer(data=request.data)
#         serialise.is_valid(raise_exception=True)
#         serialise.save()
#         return Response(serialise.data, status=status.HTTP_201_CREATED)
    
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serialise = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serialise.data)
#     elif request.method == 'POST':
#         serialise = ProductSerializer(data=request.data)
#         serialise.is_valid(raise_exception=True)
#         serialise.save()
#         return Response(serialise.data, status=status.HTTP_201_CREATED)

# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({"error": "Cannot delete a product with associated orders"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductDetails(APIView):

#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serialise = ProductSerializer(product)
#         return Response(serialise.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serialise = ProductSerializer(product, data=request.data)
#         serialise.is_valid(raise_exception=True)
#         serialise.save()
#         return Response(serialise.data)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({"error": "Cannot delete a product with associated orders"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_details(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serialise = ProductSerializer(product)
#         return Response(serialise.data)
#     elif request.method == 'PUT':
#         serialise = ProductSerializer(product, data=request.data)
#         serialise.is_valid(raise_exception=True)
#         serialise.save()
#         return Response(serialise.data)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({"error": "Cannot delete a product with associated orders"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({"error: Collection cannot be deleted because it is assigned to existing products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({"error: Collection cannot be deleted because it is assigned to existing products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer


# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serialise = CollectionSerializer(queryset, many=True, context={'request': request})
#         return Response(serialise.data)
#     elif request.method == 'POST':
#         serialise = CollectionSerializer(data=request.data)
#         serialise.is_valid(raise_exception=True)
#         serialise.save()
#         return Response(serialise.data, status=status.HTTP_201_CREATED)


# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_details(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#     if request.method == 'GET':
#         serialise = CollectionSerializer(collection)
#         return Response(serialise.data)
#     elif request.method == 'PUT':
#         serialise = CollectionSerializer(collection, data=request.data)
#         serialise.is_valid(raise_exception=True)
#         serialise.save()
#         return Response(serialise.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({"error: Collection cannot be deleted because it is assigned to existing products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}