from django.urls import path

from .views import add_listing_view, search, index, listing



urlpatterns = [
    path('', index, name='listings'),
    path('<int:listing_id>', listing, name='listing'),
    path('search', search, name='search'),
    path('add-listing', add_listing_view, name='add_listing'),
]