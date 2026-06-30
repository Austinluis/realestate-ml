from django.db import models
from accounts.models import User
from properties.models import Property

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='predictions')
    # Input features snapshot
    area = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    stories = models.IntegerField()
    mainroad = models.CharField(max_length=3)
    guestroom = models.CharField(max_length=3)
    basement = models.CharField(max_length=3)
    hotwaterheating = models.CharField(max_length=3)
    airconditioning = models.CharField(max_length=3)
    parking = models.IntegerField()
    prefarea = models.CharField(max_length=3)
    furnishingstatus = models.CharField(max_length=20)
    # Result
    predicted_price = models.FloatField()
    model_used = models.CharField(max_length=50, default='best_model')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'predictions_prediction'
        ordering = ['-created_at']

    def __str__(self):
        return f'Prediction #{self.id} by {self.user.email} — ₦{self.predicted_price:,.0f}'
