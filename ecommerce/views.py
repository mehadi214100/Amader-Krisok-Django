from django.shortcuts import render,redirect
from .models import SellerApplication,Product,ProductCategory,Cart,CartItem
from django.contrib import messages
from .forms import ProductForm

def market(request):
    products = Product.objects.all().filter(is_available = True)
    categories = ProductCategory.objects.all()
    totalItem = 0
    if request.user.is_authenticated:
        totalItem = CartItem.objects.filter(user=request.user).count()
    else:
        cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        if cart:
            totalItem = CartItem.objects.filter(cart=cart).count()
    context = {
        "products":products,
        'categories':categories,
        'totalItem':totalItem
    }
    return render(request,'market.html',context)


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
        product.product_name = request.POST.get('product_name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.unit = request.POST.get('unit')
        product.is_available = request.POST.get('is_available') == 'True'

        if 'image' in request.FILES:
                product.image = request.FILES['image']
        
        messages.success(request,"সফল ভাবে আপডেট করা হয়েছে ")

        product.save()
        return redirect('userProfile')

def delete_Product(request,product_id):
    
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.warning(request,"পন্য ডিলিট করা হয়েছে ")
    return redirect('userProfile')


def _cart_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    if current_user.is_authenticated:
        cart_item = CartItem.objects.filter(product=product,user = current_user)
        if cart_item.exists():
            cart_item = cart_item.first()
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(product=product, quantity=1, user=current_user)
    else:
        cart_id = _cart_id(request)
        cart,created = Cart.objects.get_or_create(cart_id=cart_id)
        cart_item = CartItem.objects.filter(product=product,cart=cart)

        if cart_item.exists():
            item = cart_item.first()
            item.quantity += 1
            item.save()
        else:
            CartItem.objects.create(product=product, quantity=1, cart=cart)
    

    return redirect('market')

def viewcart(request):
    
    currenet_user = request.user
    cart_items = []
    total_price = 0

    if currenet_user.is_authenticated:
        print("Cart id : ",_cart_id(request))
        cart_items = CartItem.objects.all().filter(user = currenet_user)
    else:
        cart = Cart.objects.filter(cart_id = _cart_id(request)).first()
        if cart:
            cart_items = CartItem.objects.all().filter(cart = cart)
    
    for item in cart_items:
        total_price += item.product.price * item.quantity
    
    context = {
        'total_price':total_price,
        'cart_items':cart_items,
        'grand_total':total_price+120,
    }

    return render(request,'cart.html',context)


def increment(request,product_id):
    currentUser = request.user
    product = Product.objects.get(id=product_id)

    if currentUser.is_authenticated:
        cartItem = CartItem.objects.filter(product=product,user=currentUser).first()
        if cartItem:
            cartItem.quantity += 1
            cartItem.save()
    else:
        cart = Cart.objects.filter(cart_id = _cart_id(request)).first()
        if cart:
            cartItem = CartItem.objects.filter(cart=cart,product=product).first()
            if cartItem:
                cartItem.quantity += 1
                cartItem.save()
        
    return redirect('viewcart')
def decrement(request,product_id):
    currentUser = request.user
    product = Product.objects.get(id=product_id)

    if currentUser.is_authenticated:
        cartItem = CartItem.objects.filter(product=product,user=currentUser).first()
        if cartItem:
            if cartItem.quantity > 1:
                cartItem.quantity -= 1
                cartItem.save()
            else:
                cartItem.delete()
    else:
        cart = Cart.objects.filter(cart_id = _cart_id(request)).first()
        if cart:
            cartItem = CartItem.objects.filter(cart=cart,product=product).first()
            if cartItem:
                if cartItem.quantity > 1:
                    cartItem.quantity -= 1
                    cartItem.save()
                else:
                    cartItem.delete()
        
    return redirect('viewcart')

def removeItem(request,product_id):
    currentUser = request.user
    product = Product.objects.get(id=product_id)

    if currentUser.is_authenticated:
        cartItem = CartItem.objects.filter(product=product,user=currentUser).first()
        if cartItem:
                cartItem.delete()
    else:
        cart = Cart.objects.filter(cart_id = _cart_id(request)).first()
        if cart:
            cartItem = CartItem.objects.filter(cart=cart,product=product).first()
            if cartItem:
                cartItem.delete()
        
    return redirect('viewcart')

def removeCart(request):
    currentUser = request.user

    if currentUser.is_authenticated:
        cartItem = CartItem.objects.filter(user=currentUser)
        if cartItem.exists():
                cartItem.delete()
    else:
        cart = Cart.objects.filter(cart_id = _cart_id(request)).first()
        if cart:
            CartItem.objects.filter(cart=cart).delete()
            cart.delete()
        
    return redirect('viewcart')

def merge_cart(request,user,old_session_id):
    
    cart = Cart.objects.filter(cart_id=old_session_id).first()

    if cart:
        cart_item = CartItem.objects.filter(cart=cart)

        for item in cart_item:
            existing_item = CartItem.objects.filter(product=item.product, user=user).first()

            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
                item.delete()
            else:
                item.user = user
                item.cart = None
                item.save()
        cart.delete()