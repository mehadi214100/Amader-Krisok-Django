from django.urls import path
from . import views

urlpatterns = [
    path('',views.officers,name="book_officers"),
    path('<int:officer_id>/book/',views.book_officer,name="book_officers_by_user"),
    path('approve_booking/<int:booking_id>',views.approve_booking,name="approve_booking"),
    path('approve_booking/<int:booking_id>',views.approve_booking,name="approve_booking"),
    path('cancel_booking/<int:booking_id>',views.cancel_booking,name="cancel_booking"),
]
