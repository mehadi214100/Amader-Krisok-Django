from django.urls import path
from . import views
urlpatterns = [
    path('',views.market,name="market"),
    path('apply_seller/',views.apply_seller,name="apply_seller"),
    path('add_Product/',views.add_Product,name="add_Product"),
    path('edit_Product/<int:product_id>',views.edit_Product,name="edit_Product"),
    path('delete_Product/<int:product_id>',views.delete_Product,name="delete_Product"),
]
