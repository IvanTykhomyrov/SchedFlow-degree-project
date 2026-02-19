from django.contrib import admin
from .models import Service, BusinessProfile


class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_approved')
    list_filter = ('is_approved',) # approve enabler
    search_fields = ('name',)
    list_editable = ('is_approved',) # tick to aprove

admin.site.register(Service)
admin.site.register(BusinessProfile, BusinessProfileAdmin)