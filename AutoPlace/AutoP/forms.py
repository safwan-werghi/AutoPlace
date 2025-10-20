from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import User,UserProfile
from phonenumber_field.formfields import PhoneNumberField
from django import forms
from .models import Car

class RegisterForm(UserCreationForm):
    email = models.EmailField()
    class Meta:
        model = User
        fields = ["email","password1","password2"]

class UserProfileForm(forms.ModelForm):
    # Use the PhoneNumberField from the phonenumber_field library
    phone = PhoneNumberField(required=False)
    
    # Customizing the date field with a better widget
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    
    # Adding custom validation for budget fields
    def clean(self):
        cleaned_data = super().clean()
        budget_min = cleaned_data.get('budget_min')
        budget_max = cleaned_data.get('budget_max')
        
        if budget_min and budget_max and budget_min > budget_max:
            raise ValidationError({
                'budget_min': "Minimum budget cannot be greater than maximum budget."
            })
        
        # Validate date of birth is not in the future
        dob = cleaned_data.get('date_of_birth')
        if dob and dob > date.today():
            raise ValidationError({
                'date_of_birth': "Date of birth cannot be in the future."
            })
        
        return cleaned_data
    
    class Meta:
        model = UserProfile  
        fields = [
            'phone', 'address', 'city', 'state', 'zip_code', 'country',
            'date_of_birth', 'profile_picture', 'email_notifications',
            'sms_notifications', 'preferred_contact_method', 'company_name',
            'dealer_license', 'is_verified_seller', 'budget_min', 'budget_max',
            'preferred_makes', 'preferred_body_styles'
        ]
        
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your state'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your ZIP code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'value': 'USA',  # Set default value
                'placeholder': 'Enter your country'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'preferred_contact_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your company name (if applicable)'
            }),
            'dealer_license': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your dealer license number'
            }),
            'budget_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum budget',
                'step': '0.01',
                'min': '0'
            }),
            'budget_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum budget',
                'step': '0.01',
                'min': '0'
            }),
            'preferred_makes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Toyota, Ford, Honda'
            }),
            'preferred_body_styles': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., SUV, Sedan, Truck'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sms_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_verified_seller': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        labels = {
            'phone': 'Phone Number',
            'zip_code': 'ZIP Code',
            'date_of_birth': 'Date of Birth',
            'profile_picture': 'Profile Picture',
            'email_notifications': 'Enable Email Notifications',
            'sms_notifications': 'Enable SMS Notifications',
            'preferred_contact_method': 'Preferred Contact Method',
            'company_name': 'Company Name',
            'dealer_license': 'Dealer License Number',
            'is_verified_seller': 'I am a verified seller',
            'budget_min': 'Minimum Budget',
            'budget_max': 'Maximum Budget',
            'preferred_makes': 'Preferred Vehicle Makes',
            'preferred_body_styles': 'Preferred Body Styles',
        }
        
        help_texts = {
            'phone': 'Please enter your phone number with country code',
            'preferred_makes': 'Separate multiple makes with commas',
            'preferred_body_styles': 'Separate multiple styles with commas',
        }




class CarSaleForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'Brand', 'Model', 'Year', 'price', 'mileage', 'Condition', 
            'Color', 'Fuel_Type', 'description', 'mpg_city',
            'photo1', 'photo2', 'photo3', 'photo4',
            'photo5', 'photo6', 'photo7', 'photo8'
        ]
        widgets = {
            'Brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Toyota, Ford, BMW'
            }),
            'Model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Camry, F-150, X5'
            }),
            'Year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1900,
                'max': 2025
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'mileage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'Condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Red, Blue, Black'
            }),
            'Fuel_Type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your car, its features, condition, and any other relevant details...'
            }),
            'mpg_city': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'City MPG (miles per gallon)'
            }),
            # Remove the URLInput widgets for file fields
        }
        labels = {
            'mpg_city': 'MPG (City)',
            'photo1': 'Primary Photo',
            'photo2': 'Photo 2',
            'photo3': 'Photo 3',
            'photo4': 'Photo 4',
            'photo5': 'Photo 5',
            'photo6': 'Photo 6',
            'photo7': 'Photo 7',
            'photo8': 'Photo 8',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the first photo required
        self.fields['photo1'].required = True
        self.fields['Brand'].required = True
        self.fields['Model'].required = True
        self.fields['Year'].required = True
        self.fields['price'].required = True
        
        # Add help text for file fields
        self.fields['photo1'].help_text = "Required. Upload the primary photo of your car."
        for i in range(2, 9):
            field_name = f'photo{i}'
            self.fields[field_name].help_text = "Optional. Additional photos help sell your car faster."