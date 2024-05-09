from django.urls import path

from .views import add_listing_view, search, index, listing_by_id_view, delete_listing_view, edit_listing_view



urlpatterns = [
    path('', index, name='listings'),
    path('<int:listing_id>', listing_by_id_view, name='listing'),
    path('search', search, name='search'),
    path('add-listing', add_listing_view, name='add_listing'),
    path('edit-listing/<int:listing_id>/', edit_listing_view, name='edit-listing'),
    path('delete-listing/<int:listing_id>/', delete_listing_view, name='delete-listing'),

]