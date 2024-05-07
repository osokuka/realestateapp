from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Realtor
from listings.models import Listing

def realtor_profile(request, realtor_id):
    realtor = get_object_or_404(Realtor, pk=realtor_id)
    listings = Listing.objects.filter(realtor=realtor).order_by('-list_date')
    context = {
        'realtor': realtor,
        'listings': listings
    }
    return render(request, 'realtors/profile.html', context)