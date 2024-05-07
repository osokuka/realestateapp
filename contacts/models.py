from django.db import models
from datetime import datetime
from listings.models import Listing

class Contact(models.Model):
  listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=100)
  phone = models.CharField(max_length=100)
  message = models.TextField(blank=True)
  contact_date = models.DateTimeField(default=datetime.now, blank=True)
  user_id = models.IntegerField(blank=True)
  def __str__(self):
    return self.name