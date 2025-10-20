from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RegisterForm,UserProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import UserProfile
from django.db.models import Q
from .models import Car
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car
from .forms import CarSaleForm
from django.db.models import Q  
from .models import Car

def home(response):
    return render(response,"AutoP/home.html",{})


from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save()
            login(response, user)  
            return redirect("/create_profile/")
    else:   
        form = RegisterForm()
    return render(response,"AutoP/register.html",{"form":form})


@login_required  
def createProfile(request):  
    
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            userProfile = form.save(commit=False)
            userProfile.user = request.user 
            userProfile.save()  
            messages.success(request, 'Your profile has been Created successfully!')
            return redirect("/home")
    else:   
        form = UserProfileForm(instance=profile)
    
    return render(request, "AutoP/profile_creation.html", {"form": form})



def car_listings(request):
    
    cars = Car.objects.filter(status='Available').order_by('-id')
    
    
    search_query = request.GET.get('search', '')
    if search_query:
        cars = cars.filter(
            Q(Brand__icontains=search_query) |
            Q(Model__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    
    condition_filter = request.GET.get('condition', '')
    if condition_filter:
        cars = cars.filter(Condition=condition_filter)
    
    fuel_filter = request.GET.get('fuel_type', '')
    if fuel_filter:
        cars = cars.filter(Fuel_Type=fuel_filter)
    
    
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        cars = cars.order_by('price')
    elif sort_by == 'price_high':
        cars = cars.order_by('-price')
    elif sort_by == 'mileage_low':
        cars = cars.order_by('mileage')
    elif sort_by == 'mileage_high':
        cars = cars.order_by('-mileage')
    elif sort_by == 'year_new':
        cars = cars.order_by('-Year')
    elif sort_by == 'year_old':
        cars = cars.order_by('Year')
    else:  
        cars = cars.order_by('-id')
    
    
    conditions = Car.objects.values_list('Condition', flat=True).distinct()
    fuel_types = Car.objects.values_list('Fuel_Type', flat=True).distinct()
    
    context = {
        'cars': cars,
        'search_query': search_query,
        'conditions': conditions,
        'fuel_types': fuel_types,
        'sort_by': sort_by,
        'condition_filter': condition_filter,
        'fuel_filter': fuel_filter,
    }
    
    return render(request, 'AutoP/car_listings.html', context)




@login_required
def add_car(request):
    if request.method == 'POST':
        
        form = CarSaleForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.status = 'Available'
            car.save()
            messages.success(request, 'Your car has been listed successfully!')
            return redirect('car_listings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CarSaleForm()
    
    return render(request, 'AutoP/add_car.html', {'form': form})

@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, seller=request.user)
    
    if request.method == 'POST':
        form = CarSaleForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your car listing has been updated successfully!')
            return redirect('car_detail', car_id=car.id)  # Redirect to car detail page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CarSaleForm(instance=car)
    
    return render(request, 'AutoP/add_car.html', {'form': form, 'editing': True, 'car': car})






@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id, status='Available')
    
    
    related_cars = Car.objects.filter(
        status='Available'
    ).exclude(id=car_id).filter(
        Q(Brand=car.Brand) | Q(price__range=(car.price * 0.7, car.price * 1.3))
    )[:4]
    
    context = {
        'car': car,
        'related_cars': related_cars,
    }
    return render(request, 'AutoP/car_detail.html', context)