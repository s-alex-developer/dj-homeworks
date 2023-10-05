from django.contrib import admin

from phones.models import Phone


# Register your models here.

"""
    http://127.0.0.1:8000/admin/  
    user: admin  
    password: admin
"""

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'image', 'release_date', 'lte_exists', 'slug']
