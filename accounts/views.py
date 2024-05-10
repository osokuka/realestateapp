from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from .models import UserProfile
from listings.models import Listing
from realtors.models import Realtor

def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.save()
          messages.success(request, 'You are now registered and can log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      # Fetch the user profile to check if the user is a realtor
      user_profile = UserProfile.objects.get(user=user)
            # Store is_realtor in session
    
      request.session['is_realtor'] = user_profile.is_realtor
      if user_profile.is_realtor:
        return redirect('dashboard')
      else:
        return redirect('index')
      #messages.success(request, 'You are now logged in')
      
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')

from django.shortcuts import render
from contacts.models import Contact
from listings.models import Listing
from accounts.models import UserProfile

def dashboard(request):
    user = request.user
    context = {}

    # Check if the user has a profile and if they are a realtor
    if hasattr(user, 'profile') and user.profile.is_realtor:
        try:
            
            realtor = Realtor.objects.get(user=user)
            #lets select all listings with all info for this realtor
            realtor_listings = Listing.objects.filter(realtor=realtor).select_related('realtor')
            first_realtor_id = realtor_listings.first().realtor.id if realtor_listings.exists() else None
            print(first_realtor_id)
            #print(realtor)

            contacts = Contact.objects.filter(listing__in=realtor_listings).select_related('listing').order_by('-contact_date')
            print(contacts)        
        except Realtor.DoesNotExist:
            messages.error(request, "Realtor profile not found.")
            return redirect('some_error_page')

        contacts_with_listings = [
            {
                
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone,
                'message': contact.message,
                'contact_date': contact.contact_date.strftime('%Y-%m-%d %H:%M'),
                'listing': contact.listing.title
            }
            for contact in contacts
        ]
        context['contacts_with_listings'] = contacts_with_listings
        context['realtor_listings'] = realtor_listings
        context['first_realtor_id'] = first_realtor_id

    else:
        # For regular users, fetch their inquiries
        user_contacts = Contact.objects.filter(user_id=user.id).order_by('-contact_date').select_related('listing')

        user_contacts_details = [
            {
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone,
                'message': contact.message,
                'contact_date': contact.contact_date.strftime('%Y-%m-%d %H:%M'),
                'listing': contact.listing.title
            }
            for contact in user_contacts
        ]
        context['user_contacts'] = user_contacts_details

      

    return render(request, 'accounts/dashboard.html', context)
    