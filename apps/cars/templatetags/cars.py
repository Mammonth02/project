from django import template
from django.shortcuts import render
from apps.cars.models import *
from datetime import date, time



register = template.Library()

@register.simple_tag()
def time():
    now = date.today()
    return now