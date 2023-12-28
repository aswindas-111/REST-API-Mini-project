from django.urls import path
from . views import Booklist, BookDetail


urlpatterns = [
    path('booklist',Booklist.as_view(),name='booklist'),
    path('bookdetails/<int:pk>',BookDetail.as_view(),name='bookdetails'),
]
