from django.shortcuts import render
from django.contrib import messages
from accounts.qr_code import generate_qr
from django.urls import reverse


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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RealtorProfileForm
from urllib.parse import urlparse, urlunparse

@login_required
def edit_realtor_profile(request):
    realtor = request.user.realtor  # Assuming a OneToOne link from User to Realtor
    realtor_photo = realtor.photo
    # Generate the full URL to the realtor's profile
    profile_url = request.build_absolute_uri(reverse('realtor_profile', args=[realtor.id]))
    
    # Parse the URL, replace the hostname and port
    #url_parts = urlparse(profile_url)
    #new_netloc = "tetregu.com"
    #new_url_parts = url_parts._replace(netloc=new_netloc)
    #profile_url = urlunparse(ur)
    
    # Generate QR code from the URL
    qr_code = generate_qr(profile_url)

    if request.method == 'POST':
        form = RealtorProfileForm(request.POST, request.FILES, instance=realtor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard')  # Redirect to a relevant page
    else:
        form = RealtorProfileForm(instance=realtor)

    context = {
        'form': form,
        'qr_code': qr_code,
        'photo' : realtor_photo
    }
    return render(request, 'realtors/edit_profile.html', context)
