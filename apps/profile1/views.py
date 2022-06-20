from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.views import generic
from apps.cars.models import *
from forms import *
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your views here.

def dashboard(request):
    return render(request, 'profile/dashboard.html')

def favorites(request):
    like_auto = Auto_like.objects.filter(user = request.user)
    reviewses = {}

    auto = []
    for i in like_auto:
        auto.append(i.auto)

    for i in auto:
        reviewses[i] = Reviews.objects.filter(auto = i)

    len_r = {}
    star_r = {}
    for k, v in reviewses.items():
        len_r[k.id] = len(v)
        len_c = []
        for rev in v:
            r = round((rev.comfort + rev.performance + rev.exterior_styling + rev.interior_design + rev.value_for_the_money +rev.reliability) / 6)
            len_c.append(r)
        star = 0
        for i in len_c:
            star += i
        if len(len_c) != 0:
            star_r[k.id] = round(star / len(len_c), 1)
        else:
            star_r[k] = 'нет отзывов'
    rrr = [0.5, 1.5, 2.5, 3.5, 4.5]

    paginator = Paginator(auto, 6)
    page_number = request.GET.get('page')
    auto = paginator.get_page(page_number)

    context = {
        'auto': auto,
        'len_r': len_r,
        'star_r': star_r,
        'rrr': rrr,
        
    }
    return render(request, 'profile/favorites.html', context)

def listing(request):
    context = {}
    cars = Auto.objects.filter(user = request.user)

    paginator = Paginator(cars, 6)
    cars_new = Paginator(Auto.objects.filter(user = request.user, сondition = 'new'), 6)
    cars_used = Paginator(Auto.objects.filter(user = request.user, сondition = 'used'), 6)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    cars_new = cars_new.get_page(page_number)
    cars_used = cars_used.get_page(page_number)

    context['cars'] = cars  
    context['cars_new'] = cars_new
    context['cars_used'] = cars_used
    

    return render(request, 'profile/listing.html', context=context)

def messages(request):
    return render(request, 'profile/messages.html')

def listings(request):
    context = {}
    if request.method == 'POST':
        form = AddAutoForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save() 
    else:
        form = AddAutoForm()
    context['form'] = form

    return render(request, 'profile/listings.html', context)

def delete(request, id):
        auto = Auto.objects.get(id=id)
        auto.delete()
        return HttpResponseRedirect("/")

class Ubd_post(generic.UpdateView):
    model = Auto
    form_class = AddAutoForm
    template_name = 'profile/listings.html'
    context_object_name = 'form'
    success_url = reverse_lazy('home')

class Ubd_user(generic.UpdateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'profile/profile.html'
    context_object_name = 'form'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')