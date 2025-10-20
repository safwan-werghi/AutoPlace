from django.db import models

# Create your models here.

class CarPrediction(models.Model):
    company = models.CharField(max_length=100)
    horsepower = models.FloatField()
    torque = models.FloatField()
    performance = models.FloatField()
    total_speed = models.FloatField()
    engine_cc = models.FloatField()
    fuel_type = models.CharField(max_length=50)
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company} - ${self.predicted_price:,.2f}"