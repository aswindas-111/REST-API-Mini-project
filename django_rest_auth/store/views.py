from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from store.models import Book
from store.serializers import BookSerializer

# Create your views here.

class Booklist(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    
    queryset = Book.objects.all()
    serializer_class=BookSerializer
    
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    
    queryset = Book
    serializer_class=BookSerializer
