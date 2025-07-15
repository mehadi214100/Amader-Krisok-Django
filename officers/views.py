from django.shortcuts import render,redirect
from .models import Officer,OfficerBook
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


