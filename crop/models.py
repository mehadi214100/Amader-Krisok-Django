from django.db import models
from ckeditor.fields import RichTextField
from unidecode import unidecode
from django.utils.text import slugify

class category(models.Model):
    category_name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True,max_length=150,blank=True)
    category_image = models.ImageField(upload_to='categories')
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ফসলের নাম"
        verbose_name_plural = "ফসলের নাম সমূহ"

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.category_name))
        super().save(*args,**kwargs)

    def __str__(self):
        return self.category_name
    

TYPE_CHOICES = [
        ('hybrid', 'হাইব্রিড'),
        ('high_yielding', 'উচ্চ ফলনশীল'),
        ('local', 'স্থানীয় জাত'),
        ('irri', 'আইআরআরআই জাত'),
    ]

class CropVarity(models.Model):
    crop = models.ForeignKey(category,on_delete=models.CASCADE,related_name="varieties",verbose_name="ফসলের নাম")
    varity_name = models.CharField(max_length=150,verbose_name="জাতের নাম")
    slug = models.SlugField(unique=True,max_length=150,blank=True)
    image = models.ImageField(upload_to="variety_images")
    verity_type = models.CharField(max_length=200,choices=TYPE_CHOICES,verbose_name="জাতের ধরন")
    duration = models.CharField(max_length=150,verbose_name="সময়কাল")
    yield_amount = models.CharField(
        verbose_name="গড় ফলন",
        help_text="টন/হেক্টরে"
    )
    year_released = models.CharField(verbose_name="উদ্ভাবনের বছর")
    institute = models.CharField(max_length=200, verbose_name="উদ্ভাবক প্রতিষ্ঠান")
    suitable_area = models.TextField(verbose_name="প্রস্তাবিত এলাকা")
    grain_type = models.CharField(max_length=100, verbose_name="দানাদার ধরন")
    is_popular = models.BooleanField(default=False, verbose_name="জনপ্রিয় জাত")
    is_new = models.BooleanField(default=False, verbose_name="নতুন জাত")
    additional_info = models.TextField(blank=True, null=True,verbose_name="অতিরিক্ত তথ্য")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.varity_name))
        
        super().save(*args,**kwargs)
    class Meta:
            verbose_name = "জাতের তথ্য"
            verbose_name_plural = "জাতের তথ্যসমূহ"
        
    def __str__(self):
        return self.varity_name


class CultivationMethod(models.Model):
    varity = models.OneToOneField(CropVarity,on_delete=models.CASCADE,related_name="cultivation_info")
    body = RichTextField(verbose_name="সম্পূর্ণ চাষ পদ্ধতি")

    def __str__(self):
        return f"{self.varity.varity_name}- cultivation"
    
class Fertilizer(models.Model):
    variety = models.ForeignKey(CropVarity, on_delete=models.CASCADE, related_name='fertilizers')
    name = models.CharField(max_length=100,verbose_name="সার এর নাম")
    amount_per_hectare = models.CharField(max_length=100,verbose_name="পরিমান") 

    def __str__(self):
        return f"{self.variety.varity_name} - {self.name}"

class DiseasePestInfo(models.Model):
    variety = models.OneToOneField(CropVarity, on_delete=models.CASCADE, related_name='disease_info')
    major_diseases = models.TextField(verbose_name="প্রধান রোগ") 
    major_pests = models.TextField(verbose_name="প্রধান পোকা") 
    advice = models.TextField(blank=True, null=True,verbose_name="পরামর্শ দিন")

    def __str__(self):
        return f"{self.variety.varity_name} - Disease & Pest"
    


class DiseaseInfo(models.Model):
    crop_name = models.ForeignKey(category, on_delete=models.CASCADE, related_name='all_disease_info',verbose_name="ফসলের নাম")
    disease_name = models.CharField(max_length=100, verbose_name="রোগের নাম")
    slug = models.SlugField(unique=True,blank=True,max_length=200)
    description = models.TextField(blank=True,verbose_name="সার সংক্ষেপ")
    symptoms = models.TextField(verbose_name="রোগের লক্ষণ")
    causes = models.TextField(blank=True, null=True, verbose_name="রোগের কারণ")
    prevention = models.TextField(blank=True, null=True, verbose_name="প্রতিকার")
    treatment =RichTextField(blank=True, null=True, verbose_name="চিকিৎসা বা ব্যবস্থাপনা")
    image = models.ImageField(upload_to='disease_images/', blank=True, null=True, verbose_name="রোগের ছবি")
    
    is_major = models.BooleanField(default=False, verbose_name="প্রধান রোগ?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "রোগের তথ্য"
        verbose_name_plural = "রোগের তথ্যসমূহ"

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.disease_name))
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.disease_name} - {self.crop_name.category_name}"
