from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
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
    #check if listing is owned by realtor
    if request.user.is_authenticated:
        realtor = Realtor.objects.get(user=request.user)
        listing = Listing.objects.get(id=listing_id)
        if listing.realtor != realtor:
            messages.error(request, 'You are not authorized to edit this listing.')
            return HttpResponseRedirect(reverse('dashboard'))  

    listing = get_object_or_404(Listing, pk=listing_id)

    print(request.FILES)  # See what files are being received

    if request.method == 'POST':

        lat_long = request.POST.get('lat_long', '').split(',')
        listing.latitude = float(lat_long[0].strip()) if len(lat_long) > 1 else listing.latitude
        listing.longitude = float(lat_long[1].strip()) if len(lat_long) > 1 else listing.longitude
        # Assuming you have a form to handle the data. Adjust the fields as necessary.
        listing.title = request.POST.get('title', listing.title)
        listing.address = request.POST.get('address', listing.address)
        listing.city = request.POST.get('city', listing.city)
        listing.state = request.POST.get('state', listing.state)
        listing.zipcode = request.POST.get('zipcode', listing.zipcode)
        listing.latitude = request.POST.get('latitude', listing.latitude)
        listing.longitude = request.POST.get('longitude', listing.longitude)
        #listing.google_location = request.POST.get('google_location', listing.google_location)
        listing.cadastral_record = request.POST.get('cadastral_record', listing.cadastral_record)
        listing.price = request.POST.get('price', listing.price)
        listing.bedrooms = request.POST.get('bedrooms', listing.bedrooms)
        listing.bathrooms = request.POST.get('bathrooms', listing.bathrooms)
        listing.sqft = request.POST.get('sqft', listing.sqft)
        listing.is_published = request.POST.get('is_published') == 'on'
        listing.list_date = request.POST.get('list_date', listing.list_date)
        listing.type = request.POST.get('type', listing.type)
        listing.lot_size = request.POST.get('lot_size', listing.lot_size)
        listing.garage = request.POST.get('garage', listing.garage)
        listing.description = request.POST.get('description', listing.description)
        listing.virtual_tour = request.POST.get('virtual_tour', listing.virtual_tour)
        #if no photo added do not update current fields
        if 'photo_main' in request.FILES:
            listing.photo_main = request.FILES['photo_main']
        for i in range(1, 10):  # Assuming a maximum of 9 additional photos
            photo_key = f'photo_{i}'
            if photo_key in request.FILES:
                setattr(listing, photo_key, request.FILES[photo_key])

        listing.save()
        messages.success(request, 'Listing updated successfully!')
        return redirect('dashboard')  # Redirect to the dashboard
    else:
        context = {
            'listing': listing,
            'state_choices': state_choices,
            'cities_choices': cities_choices
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

  # Keywords - handle multiple delimiters
  import re
  from django.db.models import Q

  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
        # Split the keywords string by any non-word character
        keyword_list = re.split(r'\W+', keywords)  # \W+ matches one or more non-word characters
        keyword_list = [word for word in keyword_list if word]  # Remove empty strings
        if keyword_list:  # Check if there are any keywords after splitting
            query = Q(description__icontains=keyword_list[0])  # Start with the first keyword
            for keyword in keyword_list[1:]:  # Iterate over the rest of the keywords
                query |= Q(description__icontains=keyword)  # Use OR to combine queries
            queryset_list = queryset_list.filter(query)

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
from html.parser import HTMLParser



class IframeSrcExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.src = None

    def handle_starttag(self, tag, attrs):
        if tag == "iframe":
            for attr in attrs:
                if attr[0] == "src":
                    self.src = attr[1]



@login_required
def add_listing_view(request):
    #load choices for state and city
    from .choices import state_choices, cities_choices
    state_choices = state_choices
    cities_choices = cities_choices

    #create a 16 digit random hash, combined with another 32 digit random hash
    
    #print(hash_code)
    if request.method == 'POST':
        user_id = request.user
        try:
            realtor = Realtor.objects.get(user_id=user_id)
        except Realtor.DoesNotExist:
            messages.error(request, 'Profili realtorit nuk eshte aktivizuar, kontaktoni realestate@prosolutions-ks.com.')
            return redirect('dashboard')

        lat_long = request.POST.get('lat_long', '').split(',')
        latitude = float(lat_long[0].strip()) if len(lat_long) > 1 else None
        longitude = float(lat_long[1].strip()) if len(lat_long) > 1 else None
        # Create a new listing instance from POST data
        new_listing = Listing(
            realtor=realtor,
            title=request.POST['title'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            latitude=latitude,
            longitude=longitude,
            #google_location=google_location_url,
            cadastral_record=request.POST['cadastral_record'],
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
            virtual_tour=request.POST['virtual_tour']
        )
        
        for i in range(1, 10):  # Assuming a maximum of 9 additional photos
            photo_key = f'photo_{i}'
            if photo_key in request.FILES:
                setattr(new_listing, photo_key, request.FILES[photo_key])
        
        #print(new_listing)
        new_listing.save()
        messages.success(request, 'Your listing has been successfully created!')
        return redirect('dashboard')
    else:
    
        context = {
            'state_choices': state_choices,
            'cities_choices': cities_choices
        }
        return render(request, 'listings/add_listing.html', context)
