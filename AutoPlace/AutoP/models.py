from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

class CustomAccountManager(BaseUserManager):  # ← MUST inherit from BaseUserManager

    def create_user(self, email, first_name, last_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, password, **other_fields):  # ← Correct method name
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:  # ← True (capital T)
            raise ValueError(_('Superuser must have is_staff=True'))
        
        if other_fields.get('is_superuser') is not True:  # ← True (capital T)
            raise ValueError(_('Superuser must have is_superuser=True'))

        return self.create_user(email, first_name, last_name, password, **other_fields)




class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)  # Fixed max_length
    
    # Status flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email  # ← Changed from self.user_name to self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
    







class Car(models.Model):
    CONDITION_CHOICES = [ ('New', 'New'), ('Used', 'Used'), ('Certified', 'Certified Pre-owned'),]
    FUEL_TYPE = [ ('Gasoline','Gasoline'), ('Diesel','Diesel'),('Electric','Electric'),]
    LISTING_STATUS = [ ('Available','Available'),('Pending','Pending'),('Sold','Sold'),]
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Seller",null=False)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='Buyer')
    Brand = models.CharField(max_length=200)
    Model = models.CharField(max_length=200)
    Year = models.IntegerField()
    price = models.IntegerField()
    mileage = models.IntegerField()
    Condition = models.CharField(max_length=20,choices=CONDITION_CHOICES,default='Used') 
    Color = models.CharField(max_length=20)
    Fuel_Type = models.CharField(max_length=20,choices=FUEL_TYPE,default='Gasoline') 
    description = models.CharField(max_length=250)
    photo1 = models.ImageField(upload_to='car_photos/', null=True, blank=True)
    photo2 = models.ImageField(upload_to='car_photos/', null=True, blank=True)
    photo3 = models.ImageField(upload_to='car_photos/', null=True, blank=True)
    photo4 = models.ImageField(upload_to='car_photos/', null=True, blank=True)
    photo5 = models.ImageField(upload_to='car_photos/', null=True, blank=True)
    photo6 = models.ImageField(upload_to='car_photos/', null=True, blank=True)
    photo7 = models.ImageField(upload_to='car_photos/', null=True, blank=True)
    photo8 = models.ImageField(upload_to='car_photos/', null=True, blank=True)
    mpg_city = models.IntegerField()
    status = models.CharField(max_length=20,choices=LISTING_STATUS,default='Available') 

    def _str_(self):
        return self.name
    

    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Contact Information
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    phone_verified = models.BooleanField(default=False)
    
    # Address
    address = models.TextField(null=True,blank=True)
    city = models.CharField(null=True,max_length=100, blank=True)
    state = models.CharField(null=True,max_length=100, blank=True)
    zip_code = models.CharField(null=True,max_length=20, blank=True)
    country = models.CharField(null=True,max_length=100, blank=True, default='USA')
    
    # Personal
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Communication preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    # Combined buying/selling preferences
    preferred_contact_method = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp')
    ], default='email')
    
    # Seller-related fields (optional - only for those who sell)
    company_name = models.CharField(null=True,max_length=200, blank=True)
    dealer_license = models.CharField(null=True,max_length=100, blank=True)
    is_verified_seller = models.BooleanField(default=False)
    
    # Buyer-related fields (optional - for all users)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    preferred_makes = models.CharField(null=True,max_length=500, blank=True)
    preferred_body_styles = models.CharField(null=True,max_length=200, blank=True)
    
    # Statistics (track both buying and selling activity)
    cars_listed = models.IntegerField(null=True,default=0)
    cars_sold = models.IntegerField(null=True,default=0)
    cars_bought = models.IntegerField(null=True,default=0)
    total_inquiries = models.IntegerField(null=True,default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.first_name} {self.user.last_name}"
    
    @property
    def is_seller(self):
        """Check if user has seller credentials"""
        return bool(self.company_name or self.dealer_license)
    
    @property
    def seller_rating(self):
        """Calculate seller rating (you can implement this later)"""
        return 4.5  # Placeholder



def create_profile(sender,instance,created, **kwargs):
    if created:
        #UserProfile.objects.get_or_create(user=instance)
        user_profile = UserProfile(user=instance)
        user_profile.save()


post_save.connect(create_profile,sender=User)
