from django.urls import path
from . import views

urlpatterns = [
    path('',views.officers,name="book_officers"),
    path('<int:officer_id>/book/',views.book_officer,name="book_officers_by_user"),
]
