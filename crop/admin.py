from django.contrib import admin
from .models import (
    category,
    CropVarity,
    CultivationMethod,
    Fertilizer,
    DiseasePestInfo,
    DiseaseInfo,
)

@admin.register(DiseaseInfo)
class DiseaseInfoAdmin(admin.ModelAdmin):
    list_display = ('disease_name','description','is_major')

@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'created_at')


class FertilizerInline(admin.TabularInline):
    model = Fertilizer
    extra = 1


class CultivationMethodInline(admin.StackedInline):
    model = CultivationMethod
    extra = 0
    max_num = 1


class DiseasePestInfoInline(admin.StackedInline):
    model = DiseasePestInfo
    extra = 0
    max_num = 1


@admin.register(CropVarity)
class CropVarityAdmin(admin.ModelAdmin):
    list_display = ('varity_name', 'crop', 'verity_type', 'yield_amount', 'is_popular', 'is_new')
    list_filter = ('crop', 'verity_type', 'is_popular', 'is_new')
    search_fields = ('varity_name',)
    
    inlines = [
        CultivationMethodInline,
        DiseasePestInfoInline,
        FertilizerInline,
    ]

