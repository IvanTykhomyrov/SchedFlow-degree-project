from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, BusinessProfile, WorkingHours
from .forms import BusinessProfileForm, ServiceForm, WorkingHoursForm

@login_required
def dashboard(request):
    try:
        profile = request.user.business_profile
        services = profile.services.all() # Берем только ЕГО услуги
        return render(request, 'core/dashboard.html', {
            'profile': profile,
            'services': services,
            'is_master': True
        })
    except BusinessProfile.DoesNotExist:
        return render(request, 'core/dashboard.html', {'is_master': False})

# master profile creator
@login_required
def create_business_profile(request):
    if request.method == 'POST':
        form = BusinessProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()


            for day_num in range(7):  # Цикл от 0 (Пн) до 6 (Вс)
                WorkingHours.objects.create(
                    master=profile,
                    day_of_week=day_num,
                    # Если день 5 (Сб) или 6 (Вс) — ставим выходной
                    is_day_off=(day_num >= 5)
                )


            return redirect('dashboard')
    else:
        form = BusinessProfileForm()
    return render(request, 'core/create_profile.html', {'form': form})

# service add
@login_required
@login_required
def add_service(request):
    try:
        profile = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        return redirect('create_profile')


    if not profile.is_approved:

        return redirect('dashboard')


    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.master = profile
            service.save()
            return redirect('dashboard')
    else:
        form = ServiceForm()
    return render(request, 'core/add_service.html', {'form': form})


def index(request):
    query = request.GET.get('q')
    category_filter = request.GET.get('category')

    salons = []
    is_search = False

    if query:
        salons = BusinessProfile.objects.filter(name__icontains=query, is_approved=True)
        is_search = True
    elif category_filter:
        salons = BusinessProfile.objects.filter(category=category_filter, is_approved=True)
        is_search = True
    else:
        salons = BusinessProfile.objects.none()

    return render(request, 'core/index.html', {
        'salons': salons,
        'is_search': is_search
    })


def salon_detail(request, salon_id):
    salon = get_object_or_404(BusinessProfile, pk=salon_id)
    services = salon.services.all()
    working_hours = salon.working_hours.all().order_by('day_of_week')

    return render(request, 'core/salon_detail.html', {
        'salon': salon,
        'services': services,
        'working_hours': working_hours
    })


def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'core/detail.html', {'service': service})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def schedule_settings(request):
    try:
        profile = request.user.business_profile
    except BusinessProfile.DoesNotExist:
        return redirect('create_profile')


    hours = profile.working_hours.all().order_by('day_of_week')

    return render(request, 'core/schedule.html', {'hours': hours})



@login_required
def edit_day(request, day_id):
    hour_obj = get_object_or_404(WorkingHours, pk=day_id, master__user=request.user)

    if request.method == 'POST':
        form = WorkingHoursForm(request.POST, instance=hour_obj)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        form = WorkingHoursForm(instance=hour_obj)

    return render(request, 'core/edit_day.html', {'form': form, 'day': hour_obj})