from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

from listings.models import Listing  # Make sure to import the Listing model

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        #realtor_email = request.POST['realtor_email']

        # Retrieve the Listing object using listing_id
        listing = Listing.objects.get(id=listing_id)  # This retrieves the actual Listing object

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.filter(listing_id=listing_id, user_id=user_id).exists()
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/' + listing_id)

        # Create the Contact instance with the Listing object
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        # Send email (commented out for now)
        # send_mail(
        #     'Property Listing Inquiry',
        #     'There has been an inquiry for ' + listing.title + '. Sign into the admin panel for more info',
        #     'from_email',
        #     [realtor_email, 'another_email'],
        #     fail_silently=False
        # )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/' + listing_id)