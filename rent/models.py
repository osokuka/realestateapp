from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here


#Model to register rent listings 
class RentListing(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    rent_type = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    contact_number = models.CharField(max_length=255)
    email = models.EmailField()
    garage = models.BooleanField()
    wifi = models.BooleanField()
    hendicapped_access = models.BooleanField()
    pets = models.BooleanField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    video = models.URLField(null=True, blank=True)
    virtual_tour = models.URLField(null=True, blank=True)
    floor_plan = models.ImageField(upload_to='images/', null=True, blank=True)
    available_from = models.DateField()
    available_to = models.DateField()
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

#booking calendar
class BookingCalendar(models.Model):
    listing = models.ForeignKey(RentListing.uuid, on_delete=models.DO_NOTHING) #uuid of the listing
    datefrom = models.DateField()
    date_to = models.DateField()
    available = models.BooleanField()
    reserved_by = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, blank=True)
    date_reserved = models.DateField()
    date_booked = models.DateField()
    date_cancelled = models.DateField()
    reserved_contact = models.CharField(max_length=255)
    reserved_email = models.EmailField()
    reserved_phone = models.CharField(max_length=255)
    reserved_message = models.TextField()



