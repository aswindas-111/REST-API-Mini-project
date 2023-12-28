from django.shortcuts import render
from rest_framework import generics
from store.models import Book
from store.serializers import BookSerializer

# Create your views here.

class Booklist(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class=BookSerializer
    
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book
    serializer_class=BookSerializer
