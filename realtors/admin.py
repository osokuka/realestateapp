from django.contrib import admin
from .models import Realtor

class RealtorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_mvp', 'hire_date')
    list_display_links = ('name', 'email')
    list_editable = ('is_mvp',)
    search_fields = ('name', 'email')
    list_per_page = 25

admin.site.register(Realtor, RealtorAdmin)