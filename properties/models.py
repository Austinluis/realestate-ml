from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import User

FURNISHING_CHOICES = [
    ('furnished', 'Furnished'),
    ('semi-furnished', 'Semi-Furnished'),
    ('unfurnished', 'Unfurnished'),
]

YES_NO = [('yes', 'Yes'), ('no', 'No')]

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.FileField(
        upload_to='property_photos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
    )
    location = models.CharField(max_length=255)
    area = models.IntegerField(help_text='Area in square feet')
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    stories = models.IntegerField()
    mainroad = models.CharField(max_length=3, choices=YES_NO, default='no')
    guestroom = models.CharField(max_length=3, choices=YES_NO, default='no')
    basement = models.CharField(max_length=3, choices=YES_NO, default='no')
    hotwaterheating = models.CharField(max_length=3, choices=YES_NO, default='no')
    airconditioning = models.CharField(max_length=3, choices=YES_NO, default='no')
    parking = models.IntegerField(default=0)
    prefarea = models.CharField(max_length=3, choices=YES_NO, default='no')
    furnishingstatus = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='unfurnished')
    listed_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'properties_property'
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f'{self.title} ({self.location})'
