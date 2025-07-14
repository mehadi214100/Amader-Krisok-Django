from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_farmer', True)
        extra_fields.setdefault('is_seller', True)
        extra_fields.setdefault('is_available', True)
        extra_fields.setdefault('is_officer', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True)
    is_staff = models.BooleanField(default=False)         
    is_superuser = models.BooleanField(default=False)     
    is_active = models.BooleanField(default=True)        
    is_farmer = models.BooleanField(default=True)       
    is_seller = models.BooleanField(default=False)       
    is_available = models.BooleanField(default=False)    
    is_officer = models.BooleanField(default=False)    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return self.email

choices = (
    ('Male',"Male"),
    ('Female',"Female"),
    ('Others',"Others"),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="userprofile",on_delete=models.CASCADE)
    date_of_birth = models.CharField(max_length=150,blank=True)
    image = models.ImageField(upload_to='profileimage/',blank=True)
    gender = models.CharField(max_length=150,blank=True,choices=choices)
    city = models.CharField(max_length=50)
    address = models.TextField(blank=True)