from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from store.models import Book
from store.serializers import BookSerializer
from . pagination import CustomPageNumberPagination

# Create your views here.

class Booklist(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    pagination_class=CustomPageNumberPagination
    
    queryset = Book.objects.all()
    serializer_class=BookSerializer
    
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    
    queryset = Book
    serializer_class=BookSerializer
