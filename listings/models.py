from django.db import models
from datetime import datetime
from realtors.models import Realtor
import uuid
import os
from django.conf import settings

def upload_to(instance, filename):
    folder_name = f'photos/{instance.uuid}'
    full_path = os.path.join(settings.MEDIA_ROOT, folder_name)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return os.path.join(folder_name, filename)

class Listing(models.Model):
    uuid = models.CharField(max_length=36, default=uuid.uuid4, editable=False)
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    google_location = models.URLField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    cadastral_record = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=100, default='Shtepi')
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    virtual_tour = models.CharField(max_length=200, blank=True)
    photo_main = models.ImageField(upload_to=upload_to)
    photo_1 = models.ImageField(upload_to=upload_to, blank=True)
    photo_2 = models.ImageField(upload_to=upload_to, blank=True)
    photo_3 = models.ImageField(upload_to=upload_to, blank=True)
    photo_4 = models.ImageField(upload_to=upload_to, blank=True)
    photo_5 = models.ImageField(upload_to=upload_to, blank=True)
    photo_6 = models.ImageField(upload_to=upload_to, blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
    
