from django.shortcuts import render,redirect
from .models import SellerApplication,Product
from django.contrib import messages
from .forms import ProductForm

def market(request):
    return render(request,'market.html')


def apply_seller(request):
    if hasattr(request.user, 'seller_request'):
        messages.error(request, "আপনি ইতোমধ্যে আবেদন করেছেন।")
        return redirect('userProfile')
    else:
        if request.method == 'POST':
            land_area = request.POST.get('land_area')
            crop_types  = request.POST.get('crop_types')
            farming_experience  = request.POST.get('farming_experience')
            document  = request.FILES.get('document')

            if not land_area or not crop_types or not farming_experience:
                return redirect('userProfile')
            
            SellerApplication.objects.create(
                user = request.user,
                land_area = land_area,
                crop_types = crop_types,
                farming_experience = farming_experience,
                document = document,
                status = 'pending',
            )
            messages.success(request, "আপনার আবেদন সফলভাবে গ্রহণ করা হয়েছে।")
            return redirect('userProfile')
        

def add_Product(request):
    if(request.method == "POST"):
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('userProfile')
    else:
        form = ProductForm()
    return render(request, 'profile.html', {'Productform': form})


def edit_Product(request,product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
    else:
        form = ProductForm(instance=product)
    context = {
        "product_form":form
    }
    return redirect('userProfile',context)


def delete_Product(request,product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('userProfile')