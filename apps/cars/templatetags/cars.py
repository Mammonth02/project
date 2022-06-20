from django import template
from django.shortcuts import render
from apps.cars.models import *



register = template.Library()

# @register.simple_tag()
# def navbar():
#     like_auto = Auto_like.objects.filter(user = request.user)
#     like_len = len(like_auto)

#     return like_len