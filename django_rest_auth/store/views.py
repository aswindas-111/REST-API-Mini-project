from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from store.models import Book
from store.serializers import BookSerializer
from . pagination import CustomPageNumberPagination
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    # Invalidate the cache when a Book object is saved or deleted
    cache_key = 'book_queryset'
    cache.delete(cache_key)
class Booklist(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        cache_key = 'book_queryset'
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Book.objects.all()
            cache.set(cache_key, queryset, timeout=300)  # Cache for 5 min

        return queryset

    serializer_class = BookSerializer
    
    
    
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    
    queryset = Book
    serializer_class=BookSerializer
