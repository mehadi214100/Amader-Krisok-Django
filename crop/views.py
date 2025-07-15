from django.shortcuts import render,HttpResponse
from .models import category,CropVarity,DiseaseInfo
from django.db.models import Q

def crop_info(request):
    crops = category.objects.all()

    searchItem = request.GET.get('cropsName','')
    if searchItem:
        crops = category.objects.all().filter(
            Q(category_name__icontains = searchItem) | 
            Q(description__icontains = searchItem)
        )

    context = {
        "crops":crops,
    }
    return render(request,'crop_info.html',context)


def all_crops(request,crop_category,varity_slug=None):
    crop_cat_obj = category.objects.get(slug = crop_category)
    all_varieties = CropVarity.objects.all().filter(crop=crop_cat_obj)
    crops_info = None

    if varity_slug == None:
        crops_info = all_varieties.first()
        
    else:
        crops_info = CropVarity.objects.filter(crop=crop_cat_obj,slug = varity_slug).first()

    context = {
        "all_varieties":all_varieties,
        "crops_info":crops_info,
    }

    return render(request,'all_crops.html',context)


def disease_info(request):
    all_disease = DiseaseInfo.objects.all()
    
    searchItem = request.GET.get('diseaseName','')
    if searchItem:
        all_disease = DiseaseInfo.objects.all().filter(
            Q(disease_name__icontains = searchItem) | 
            Q(description__icontains = searchItem)
        )
    context = {
        "all_disease":all_disease,
    }
    return render(request,'disease_info.html',context)

def disease_info_details(request,disease_name):
    disease_details = DiseaseInfo.objects.get(slug = disease_name)
    context = {
        "disease_details":disease_details,
    }
    return render(request,'disease_info_details.html',context)
