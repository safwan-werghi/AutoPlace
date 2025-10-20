from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CarPrediction
from .ml_model.predictor import predictor
import json

def predict_car_price(request):
    if request.method == 'POST':
        try:
            
            print("POST data:", dict(request.POST))
            print("All POST keys:", list(request.POST.keys()))
            
            
            company_name = request.POST.get('company', '').strip()
            print(f"Raw company name: '{company_name}'")
            
            if not company_name:
                return render(request, 'car_predictor/predict.html', {
                    'error': 'Company name is required! Please enter a car company.'
                })
            
            
            try:
                horsepower = float(request.POST.get('horsepower', 0))
                torque = float(request.POST.get('torque', 0))
                performance = float(request.POST.get('performance', 0))
                total_speed = float(request.POST.get('total_speed', 0))
                engine_cc = float(request.POST.get('engine_cc', 0))
                seats = float(request.POST.get('seats', 5))
            except ValueError as e:
                return render(request, 'car_predictor/predict.html', {
                    'error': f'Invalid number format: {str(e)}'
                })
            
            fuel_type = request.POST.get('fuel_type', 'Petrol').strip()
            if not fuel_type:
                fuel_type = 'Petrol'  
            
            
            input_data = {
                'Company Names': company_name,
                'HorsePower_Clean': horsepower,
                'Torque_Clean': torque,
                'Performance_Clean': performance,
                'TotalSpeed_Clean': total_speed,
                'Engine_CC': engine_cc,
                'Fuel Types': fuel_type,
                'Seats_Clean': seats
            }
            
            print(f"Input data for prediction: {input_data}")
            
            
            predicted_price = predictor.predict_price(input_data)
            print(f"Predicted price: {predicted_price}")
            
            
            car_prediction = CarPrediction.objects.create(
                company=company_name,
                horsepower=horsepower,
                torque=torque,
                performance=performance,
                total_speed=total_speed,
                engine_cc=engine_cc,
                fuel_type=fuel_type,
                predicted_price=predicted_price
            )
            print(f"Saved to database with ID: {car_prediction.id}")
            
            
            display_data = {
                'Company_Names': company_name,
                'HorsePower_Clean': horsepower,
                'Torque_Clean': torque,
                'Performance_Clean': performance,
                'TotalSpeed_Clean': total_speed,
                'Engine_CC': engine_cc,
                'Fuel_Types': fuel_type,
                'Seats_Clean': seats
            }
            
            return render(request, 'car_predictor/result.html', {
                'predicted_price': predicted_price,
                'input_data': display_data
            })
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return render(request, 'car_predictor/predict.html', {
                'error': f'Prediction failed: {str(e)}'
            })
    
    return render(request, 'car_predictor/predict.html')

def prediction_api(request):
    """API endpoint for predictions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            predicted_price = predictor.predict_price(data)
            return JsonResponse({'predicted_price': predicted_price})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)