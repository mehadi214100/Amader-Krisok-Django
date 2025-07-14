from django.urls import path
from .import views
urlpatterns = [
    path('',views.crop_info,name="crop_info"),
    path('all_crops/<slug:crop_category>/', views.all_crops, name="all_crops"),
    path('all_crops/<slug:crop_category>/<slug:varity_slug>/',views.all_crops,name="all_crops"),
    path('disease_info',views.disease_info,name="disease_info"),
    path('disease_info/<slug:disease_name>/',views.disease_info_details,name="disease_info_details"),
    
    
]
