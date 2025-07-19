from django.urls import path
from . import views

urlpatterns = [
    path('',views.farmerandmachine,name="farmerandmachine")
]
