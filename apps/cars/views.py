from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from apps.cars.models import *
from django.views.generic.edit import CreateView
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from forms import *

# Create your views here.
def rz():
    all_cars = Auto.objects.all()
    reviewses = {}
    for i in all_cars:
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


    return [star_r, rrr, len_r, all_cars]

def index(request):
    all_cars = Auto.objects.all()
    cat = {
        'Марка': Make.objects.all(),
        'Тип': AutoType.objects.all()
    }

    auto = Auto.objects.all()[:4]

    drp = {
            'Каробка передач': set(),
            'Состояние': set(),
        }
    for a in all_cars:
            drp['Каробка передач'].add(a.transmission)
            drp['Состояние'].add(a.сondition)

    
    paginator = Paginator(all_cars, 8   )
    new_cars = Paginator(Auto.objects.filter(сondition = 'Новый'), 8)
    used_cars = Paginator(Auto.objects.filter(сondition = 'Б/У'), 8)
    page_number = request.GET.get('page')
    all_cars = paginator.get_page(page_number)
    new_cars = new_cars.get_page(page_number)
    used_cars = used_cars.get_page(page_number)

    context = {
            'all_cars': all_cars,
            'new_cars': new_cars,
            'used_cars': used_cars,
            'len_r': rz()[2],
            'star_r': rz()[0],
            'rrr': rz()[1],
            'drp': drp,
            'cat': cat,
            'type': AutoType.objects.all(),
            'auto': auto,
        }
    return render(request, 'home/index.html', context)

def single(request, id):
    car = Auto.objects.get(id = id)
    reviewses = Reviews.objects.filter(auto = car)
    try:
        like = Auto_like.objects.get(auto = car, user = request.user)
    except:
        like = None
    
    len_r = {}
    for rev in reviewses:
        r = round((rev.comfort + rev.performance + rev.exterior_styling + rev.interior_design + rev.value_for_the_money +rev.reliability) / 6)
        len_r[rev.id] = r

    c1 = {'комфорт':0, 'представление':0, 'внешний вид':0, 'дизайн интерьера':0, 'ценa и качество':0, 'надежность':0}
    for i in reviewses:
        c1['комфорт'] += i.comfort
        c1['представление'] += i.performance
        c1['внешний вид'] += i.exterior_styling
        c1['дизайн интерьера'] += i.interior_design
        c1['ценa и качество'] += i.value_for_the_money
        c1['надежность'] += i.reliability

    if len(reviewses) != 0:
        for k, v in c1.items():
            c1[k] = round(v / len(reviewses), 1)
    else:
        for k, v in c1.items():
            c1[k] = 'нет отзывов'

    rrr = [1, 2, 3, 4, 5]

    paginator = Paginator(reviewses, 4)
    page_number = request.GET.get('page')
    reviewses = paginator.get_page(page_number)
    context = {
        'car': car,
        'len_r': len_r,
        'rrr': rrr,
        'reviewses': reviewses,
        'c1': c1,
        'like': like,

    }

    if request.method == 'POST':
        form = ReviewsAddForm(request.POST)
        form_l = AutolikeForm(request.POST)
        form_m = ChatForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.auto = car
            form.save()
            return redirect('single_page', car.id)
        if form_l.is_valid():
            form_l = form_l.save(commit=False)
            form_l.user = request.user
            form_l.auto = car
            form_l.save()
            return redirect('single_page', car.id)
        if form_m.is_valid():
            form_m = form_m.save(commit=False)
            form_m.sender = request.user
            form_m.recipient = car.user
            form_m.save()
            return redirect('chat', car.user.id)
    else:
        form = ReviewsAddForm()
        form_l = AutolikeForm()
        form_m = ChatForm()

    context['form']= form
    context['form_l']= form_l
    context['form_m']= form_m
    context['len_l']= len(Auto_like.objects.filter(auto = car))


    return render(request, 'single/single_page.html', context)

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'home/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, odject_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'home/login.html'

    def get_context_data(self, *, odject_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def delete_like(request, id):
        like = Auto_like.objects.get(id=id)
        car = Auto.objects.get(id = like.auto_id)
        like.delete()
        return redirect("single_page", car.id)

class FilterObj():
    def get_cat(self):
        return {'Марка': Make.objects.all(), 'Тип': AutoType.objects.all()}

    def get_drp(self):
        auto_all =  Auto.objects.all()
        drp = {
            'Каробка передач': set(),
            'Тип привода': set(),
            'Состояние': set(),
            'Тип топлива': set(),
            'Цвет': set(),
        
        }
        for a in auto_all:
            drp['Каробка передач'].add(a.transmission)
            drp['Тип привода'].add(a.drive_type)
            drp['Состояние'].add(a.сondition)
            drp['Тип топлива'].add(a.fuel_type)
            drp['Цвет'].add(a.color)
        
        return drp
    def get_sorted(self):
        drp = {
            'год': 'year',
            'цена': 'prise',
            'пробег': 'mileage',
        }
        return drp


class AutoAll(FilterObj, generic.ListView):
    models = Auto
    queryset = Auto.objects.all()

    template_name = "filter/filter.html"
    context_object_name = 'auto_all'

    def get_context_data(self, *, odject_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['len_r'] = rz()[2]
        context['rrr'] = rz()[1]
        context['star_r'] = rz()[0]
        context['len_a'] = len(rz()[3])

        return context

class FilterAuto(FilterObj, generic.ListView):

    template_name = "filter/filter.html"
    context_object_name = 'auto_all'
    
    def get_queryset(self):
        global queryset
        queryset = Auto.objects.filter(
             make__in=self.request.GET.getlist("Марка"),
             transmission__in=self.request.GET.getlist("Каробка передач"),
             drive_type__in=self.request.GET.getlist("Тип привода"),
             сondition__in=self.request.GET.getlist("Состояние"),
             fuel_type__in=self.request.GET.getlist("Тип топлива"),
             type_auto__in=self.request.GET.getlist("Тип"),
             color__in=self.request.GET.getlist("Цвет"),
             
             prise__lte=int(self.request.GET.get("max_prise")),
             prise__gte=int(self.request.GET.get("min_prise")),

             cylinders__lte=int(self.request.GET.get("max_s")),
             cylinders__gte=int(self.request.GET.get("min_s")),

             engine_size__lte=int(self.request.GET.get("max_o")),
             engine_size__gte=int(self.request.GET.get("min_o")),

             year__lte=int(self.request.GET.get("max_year")),
             year__gte=int(self.request.GET.get("min_year")),
            ).order_by(self.request.GET.get("sorted"))
        return queryset

    def get_context_data(self, *, odject_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['len_a'] = len(queryset)
        context['len_r'] = rz()[2]
        context['rrr'] = rz()[1]
        context['star_r'] = rz()[0]

        return context

class FilterAutoIndex(FilterObj, generic.ListView):

    template_name = "filter/filter.html"
    context_object_name = 'auto_all'
    
    def get_queryset(self):
        global queryset
        queryset = Auto.objects.filter(
             make__in=self.request.GET.getlist("Марка"),
             transmission__in=self.request.GET.getlist("Каробка передач"),
             сondition__in=self.request.GET.getlist("Состояние"),
             type_auto__in=self.request.GET.getlist("Тип"),
            )   
        return queryset

    def get_context_data(self, *, odject_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['len_a'] = len(queryset)
        context['len_r'] = rz()[2]
        context['rrr'] = rz()[1]
        context['star_r'] = rz()[0]

        return context

def category_list(request, id):
    auto_all = Auto.objects.filter(type_auto_id = id)
    typs = AutoType.objects.all()
    auto = Auto.objects.all()[:3]
    make = Make.objects.all()

    paginator = Paginator(auto_all, 4)
    page_number = request.GET.get('page')
    auto_all = paginator.get_page(page_number)


    return render(request, 'category/list.html', locals())


