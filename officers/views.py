from django.shortcuts import render,redirect
from .models import Officer,OfficerBook
from ecommerce.models import SellerApplication
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid


def officers(request):
    officers = Officer.objects.all().filter(is_available = True)
    context = {
        'officers':officers,
    }
    return render(request,"book_officers.html",context)

@login_required
def book_officer(request,officer_id):
    officer = Officer.objects.get(id=officer_id)
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        date  = request.POST.get('date')
        time  = request.POST.get('time')
        discussion_content  = request.POST.get('discussion_content')

        OfficerBook.objects.create(
            user = request.user,
            officer = officer,
            phone_number = phone_number,
            date = date,
            time = time,
            discussion_content = discussion_content
        )
        messages.success(request,"Booking Successfull !!!!")

        return redirect('book_officers')
    return redirect('book_officers')

def approve_booking(request,booking_id):
    booking = OfficerBook.objects.get(id=booking_id)
    if booking.status == "cancel":
        messages.warning(request,"Already cancel !!!")
        return redirect('userProfile')
    booking.status = "approved"
    booking.meeting_link = f"https://meet.jit.si/{uuid.uuid4().hex}"
    
    booking.save()
    messages.success(request,"Approved Successfully")
    return redirect('userProfile')

def approve_seller_application(request,application_id):
    seller = SellerApplication.objects.get(id=application_id)
    if seller.status == "cancel":
        messages.warning(request,"Already cancel !!!")
        return redirect('userProfile')
    seller.user.is_seller = True
    seller.status = "approved"
    seller.approved_by = request.user
    seller.user.save()
    seller.save()
    messages.success(request,"Approved Successfully")
    return redirect('userProfile')


def cancel_booking(request,booking_id):
    booking = OfficerBook.objects.get(id=booking_id)
    if booking.status == "approved":
        messages.warning(request,"Already Approved !!!")
        return redirect('userProfile')
    booking.status = "cancel"
    booking.save()
    messages.warning(request,"Cancel Successfully !!!")
    return redirect('userProfile')

def reject_seller_application(request,application_id):
    seller = SellerApplication.objects.get(id=application_id)
    if seller.status == "approved":
        messages.warning(request,"Already Approved !!!")
        return redirect('userProfile')
    seller.status = "cancel"
    seller.delete()
    messages.warning(request,"Cancel Successfully !!!")
    return redirect('userProfile')



