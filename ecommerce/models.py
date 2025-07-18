from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from accounts.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(unique=True,max_length=150,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='productCategory/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        
        super().save(*args,**kwargs)
        
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

UNIT_CHOICES = [
    ('kg', 'কেজি'),
    ('g', 'গ্রাম'),
    ('l', '্লিটার'),
    ('pc', 'পিস'),
]

class Product(models.Model):
    product_name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True,max_length=150,blank=True,null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    image = models.ImageField(upload_to='product/')
    stock = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    unit = models.CharField(max_length=15,choices=UNIT_CHOICES)
    location = models.CharField(max_length=150)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,related_name='products')
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sellitem')
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now= True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.product_name))
        super().save(*args,**kwargs)

    def __str__(self):
        return self.product_name
    

statusChoice = (
    ('pending','Pending'),
    ('approved','Approved'),
    ('completed','Completed'),
    ('cancel','Cancel'),
    ('notapplied','Not Applied'),
)

class SellerApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_request')
    land_area = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='মোট জমির পরিমাণ (বিঘা)')
    crop_types = models.CharField(max_length=255, verbose_name='প্রধান ফসলসমূহ (কমা দিয়ে আলাদা করুন)')
    farming_experience = models.PositiveIntegerField(verbose_name='কৃষিতে অভিজ্ঞতা (বছর)')
    document = models.FileField(upload_to='documents/')
    status = models.CharField(choices=statusChoice,max_length=50,default="notapplied")
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sellerapproved',null=True)
    class Meta:
        verbose_name = 'বিক্রেতা আবেদন'
        verbose_name_plural = 'বিক্রেতা আবেদনসমূহ'

    def __str__(self):
        return self.user.first_name


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myorders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="sellingList")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    status_choices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('bkash', 'bKash')])
    shipping_address = models.TextField()
    contact_number = models.CharField(max_length=15) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.buyer.username} - {self.product.product_name} ({self.quantity})"

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
