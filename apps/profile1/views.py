from urllib import request
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.views import generic
from apps.cars.models import *
from apps.profile1.models import *
from apps.cars.views import rz
from forms import *
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your views here.

def dashboard(request):
    return render(request, 'profile/dashboard.html')

def favorites(request):
    like_auto = Auto_like.objects.filter(user = request.user)

    auto = []
    for i in like_auto:
        auto.append(i.auto)

    paginator = Paginator(auto, 6)
    page_number = request.GET.get('page')
    auto = paginator.get_page(page_number)

    context = {
        'auto': auto,
        'len_r': rz()[2],
        'rrr': rz()[1],
        'star_r': rz()[0]
        
    }
    return render(request, 'profile/favorites.html', context)

def listing(request):
    context = {}
    cars = Auto.objects.filter(user = request.user)

    paginator = Paginator(cars, 6)
    cars_new = Paginator(Auto.objects.filter(user = request.user, сondition = 'Новый'), 6)
    cars_used = Paginator(Auto.objects.filter(user = request.user, сondition = 'Б/У'), 6)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    cars_new = cars_new.get_page(page_number)
    cars_used = cars_used.get_page(page_number)

    context['cars'] = cars  
    context['cars_new'] = cars_new
    context['cars_used'] = cars_used
    

    return render(request, 'profile/listing.html', context=context)

def messages(request):
    send = Chat.objects.filter(sender = request.user)
    receive = Chat.objects.filter(recipient = request.user)
    senders = set()
    recipients = set()

    for i in receive:
        senders.add(i.sender)
    for i in send:
        recipients.add(i.recipient)
    users = senders.union(recipients)
    
    return render(request, 'profile/messages.html', locals())

def chat(request, id):
    send = Chat.objects.filter(sender = request.user)
    receive = Chat.objects.filter(recipient = request.user)
    senders = set()
    recipients = set()

    for i in receive:
        senders.add(i.sender)
    for i in send:
        recipients.add(i.recipient)
    users = senders.union(recipients)

    messages_send = Chat.objects.filter(sender_id = id, recipient = request.user)
    messages_receive = Chat.objects.filter(recipient_id = id, sender = request.user)
    messages = messages_send.union(messages_receive)

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.sender = request.user
            form.recipient_id = id
            form.save()
            return redirect('chat', id)
    else:
        form = ChatForm()
    sender = User.objects.get(id = id)
    return render(request, 'profile/messages.html', locals())

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