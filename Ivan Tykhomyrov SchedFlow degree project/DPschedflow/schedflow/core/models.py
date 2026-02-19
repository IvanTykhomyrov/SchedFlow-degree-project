from django.db import models
from django.contrib.auth.models import User

 #categories
CATEGORY_CHOICES = [
    ('barber', 'Barbershop'),
    ('nails', 'Nail Salon'),
    ('brows', 'Eyebrows & Lashes'),
    ('medical', 'Medical Center'),
    ('dentist', 'Dentist'),
    ('psycho', 'Psychotherapy'),
    ('shop', 'Shops'),
    ('auto', 'Auto Service'),
    ('spa', 'Spa Salon'),
    ('pets', 'Pet Services'),
]

#Service master profile

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')


    name = models.CharField(max_length=100, verbose_name="Business Name")


    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='barber', verbose_name="Category")


    description = models.TextField(blank=True, verbose_name="About / Description")


    address = models.CharField(max_length=200, blank=True, verbose_name="Address")


    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")

    is_approved = models.BooleanField(default=False, verbose_name="Approved by Admin")

    def __str__(self):
        return self.name


# work schedule
class WorkingHours(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
        (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'),
    ]
    master = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='working_hours')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField(default='09:00')
    end_time = models.TimeField(default='18:00')
    is_day_off = models.BooleanField(default=False)

    class Meta:
        ordering = ['day_of_week']
        unique_together = ('master', 'day_of_week')


# service
class Service(models.Model):

    master = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='services')

    name = models.CharField(max_length=100)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='barber')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField(default=60)

    def __str__(self):
        return self.name

