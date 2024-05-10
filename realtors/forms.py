from django import forms
from .models import Realtor

class RealtorProfileForm(forms.ModelForm):
    class Meta:
        model = Realtor
        fields = ['name', 'email', 'phone', 'description', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

