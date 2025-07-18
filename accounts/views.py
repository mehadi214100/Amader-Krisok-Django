from django.shortcuts import render,redirect
from .forms import RegistrationForm,ProfileForm,OfficerProfileForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .models import User,UserProfile
from django.contrib.auth.decorators import login_required
from officers.models import Officer,OfficerBook
from ecommerce.models import SellerApplication
from django.db.models import Q
from ecommerce.forms import ProductForm
from ecommerce.models import Product

def loginFunction(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "সফলভাবে লগইন হয়েছে")
            return redirect('home')  
        else:
            messages.error(request, "ভুল ইমেইল বা পাসওয়ার্ড")

    return render(request, 'login.html')

def registerFunction(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            messages.success(request, "রেজিষ্ট্রেশন সফল হয়েছে ")
            return redirect('loginFunction') 
        else:
            messages.error(request, "ফর্মে কিছু ভুল আছে। অনুগ্রহ করে আবার চেষ্টা করুন।")
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def logoutFunction(request):
    logout(request)
    return redirect("home")

from .models import UserProfile
from officers.models import Officer

@login_required
def userProfile(request):
    userinfo = request.user

    if userinfo.is_farmer:
        try:
            farmerprofile = userinfo.userprofile
        except UserProfile.DoesNotExist:
            farmerprofile = UserProfile.objects.create(user=userinfo)
    else:
        farmerprofile = None

    if userinfo.is_officer:
        try:
            officer_profile = userinfo.officer_profile
        except Officer.DoesNotExist:
            officer_profile = Officer.objects.create(user=userinfo)
    else:
        officer_profile = None

    form = None
    officer_form = None
    applications = SellerApplication.objects.all().filter(status='pending')
    if request.method == 'POST':
        if userinfo.is_officer:
            officer_form = OfficerProfileForm(request.POST, request.FILES, instance=officer_profile)
            if officer_form.is_valid():
                officer_form.save()
                return redirect('userProfile')
        elif userinfo.is_farmer:
            form = ProfileForm(request.POST, request.FILES, instance=farmerprofile)
            if form.is_valid():
                form.save()
                return redirect('userProfile')
    else:
        if userinfo.is_farmer:
            form = ProfileForm(instance=farmerprofile)
        if userinfo.is_officer:
            officer_form = OfficerProfileForm(instance=officer_profile)

    
    bookings = OfficerBook.objects.all().filter(Q(user = request.user) | Q(officer = officer_profile))

    Productform = ProductForm()
    allproducts = Product.objects.all().filter(seller = request.user)
    return render(request, 'profile.html', {
        'userinfo': userinfo,
        'form': form,
        'officer_form': officer_form,
        'profile': farmerprofile,
        'officer_profile': officer_profile,
        "bookings":bookings,
        'applications':applications,
        'Productform':Productform,
        'allproducts':allproducts,
    })
