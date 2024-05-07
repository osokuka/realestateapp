from django.urls import path
from .views import realtor_profile


urlpatterns = [
    
    path('realtors/<int:realtor_id>/', realtor_profile, name='realtor_profile'),
    
]