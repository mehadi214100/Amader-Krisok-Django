from django.urls import path
from . import views
urlpatterns = [
    path('',views.market,name="market"),
    path('viewcart/',views.viewcart,name="viewcart"),
    path('apply_seller/',views.apply_seller,name="apply_seller"),
    path('add_Product/',views.add_Product,name="add_Product"),
    path('edit_Product/<int:product_id>',views.edit_Product,name="edit_Product"),
    path('delete_Product/<int:product_id>',views.delete_Product,name="delete_Product"),
    path('add_cart/<int:product_id>',views.add_cart,name="add_cart"),
    path('increment/<int:product_id>',views.increment,name="increment"),
    path('decrement/<int:product_id>',views.decrement,name="decrement"),
    path('removeItem/<int:product_id>',views.removeItem,name="removeItem"),
    path('removeCart/>',views.removeCart,name="removeCart"),
]
