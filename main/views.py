import requests
from abc import ABC ,abstractmethod

from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import date,timedelta,datetime

from .forms import NewUserForm
from .models import UserProfile,Room,Movie,Seat,Ticket

