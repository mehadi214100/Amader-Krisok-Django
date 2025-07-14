from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.loginFunction,name="loginFunction"),
    path('register/',views.registerFunction,name="registerFunction"),
    path('logout/',views.logoutFunction,name="logoutFunction"),
    path('userProfile/',views.userProfile,name="userProfile"),
]
