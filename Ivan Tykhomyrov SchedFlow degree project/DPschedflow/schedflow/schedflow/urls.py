from django.contrib import admin
from django.urls import path, include
from core.views import index, service_detail, register, dashboard, create_business_profile, add_service, schedule_settings, edit_day, salon_detail
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index), # Главная страница
    path('dashboard/', dashboard, name='dashboard'),
    path('become-partner/', create_business_profile, name='create_profile'),
    path('add-service/', add_service, name='add_service'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('', index, name='index'),
    path('service/<int:service_id>/', service_detail, name='detail'),
    path('my-schedule/', schedule_settings, name='schedule'),
    path('my-schedule/edit/<int:day_id>/', edit_day, name='edit_day'),
    path('salon/<int:salon_id>/', salon_detail, name='salon_detail'),
]