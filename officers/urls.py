from django.urls import path
from . import views

urlpatterns = [
    path('',views.book_officers,name="book_officers")
]
