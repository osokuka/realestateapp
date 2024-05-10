from django.urls import path
from .views import realtor_profile, edit_realtor_profile


urlpatterns = [
    
    path('realtors/<int:realtor_id>/', realtor_profile, name='realtor_profile'),
    path('realtors/edit_profile/', edit_realtor_profile, name='edit_profile'),
    
]

