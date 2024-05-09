from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from accounts.models import UserProfile
from .choices import price_choices, bedroom_choices, state_choices, cities_choices
from django.shortcuts import render, redirect
from .models import Listing
from django.contrib import messages
from django.utils.timezone import datetime
from django.contrib.auth.decorators import login_required

from .models import Listing

def index(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }

  return render(request, 'listings/listings.html', context)

def listing_by_id_view(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': Listing.objects.get(pk=listing_id)
    
  }

  print(context)  
  return render(request, 'listings/listing.html', context)

@login_required
def edit_listing_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/update_listing.html', context)

from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def delete_listing_view(request, listing_id):
    #check if listing is owned by realtor
    if request.user.is_authenticated:
        realtor = Realtor.objects.get(user=request.user)
        listing = Listing.objects.get(id=listing_id)
        if listing.realtor != realtor:
            messages.error(request, 'You are not authorized to delete this listing.')
            return HttpResponseRedirect(reverse('dashboard'))  

    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        listing.delete()
        messages.success(request, 'The listing has been successfully deleted.')
        return HttpResponseRedirect(reverse('dashboard'))  # Redirect to the listings index page
    else:
        return render(request, 'listings/delete_confirm.html', {'listing_id': listing_id})

def search(request):
  queryset_list = Listing.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # State
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      queryset_list = queryset_list.filter(state__iexact=state)

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'cities_choices': cities_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET
  }

  return render(request, 'listings/search.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listing, Realtor
from django.contrib.auth.models import User

@login_required
def add_listing_view(request):
    if request.method == 'POST':
        user_id = request.user
        try:
            realtor = Realtor.objects.get(user_id=user_id)
        except Realtor.DoesNotExist:
            messages.error(request, 'Realtor profile does not exist.')
            return redirect('realtors:create')
        # Create a new listing instance from POST data
        new_listing = Listing(
            realtor=realtor,
            title=request.POST['title'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            zipcode=request.POST['zipcode'],
            price=request.POST['price'],
            bedrooms=request.POST['bedrooms'],
            bathrooms=request.POST['bathrooms'],
            sqft=request.POST['sqft'],
            photo_main=request.FILES['photo_main'],
            is_published=True,
            list_date=datetime.now(),
            type=request.POST['type'],
            lot_size=request.POST['lot_size'],
            garage=request.POST['garage'],
            description=request.POST['description'],
        )
        
        for i in range(1, 10):  # Assuming a maximum of 9 additional photos
            photo_key = f'photo_{i}'
            if photo_key in request.FILES:
                setattr(new_listing, photo_key, request.FILES[photo_key])

        new_listing.save()
        messages.success(request, 'Your listing has been successfully created!')
        return redirect('dashboard')
    else:
        return render(request, 'listings/add_listing.html')