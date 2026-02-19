from django import forms
from .models import BusinessProfile, Service, WorkingHours


class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ['name', 'category', 'description', 'address', 'phone']

#form for adding service
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'description', 'price', 'duration_minutes']

class WorkingHoursForm(forms.ModelForm):
    class Meta:
        model = WorkingHours
        fields = ['start_time', 'end_time', 'is_day_off']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'is_day_off': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }