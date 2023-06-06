from typing import Any
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

#GLOBAL VARIABLES
page = 1

#CLASS FOR HANDLING FETCHING DATA FROM API Tmbd
class APIFetcher:
    def __init__(self,api_url,endpoint):
        self.api_url = api_url
        self.endpoint = endpoint
    
    def fetch_data(self):
        url = self.api_url + self.endpoint
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def __str__(self):
        return f'API URL: {self.api_url} | ENDPOINT: {self.endpoint}'

class MovieListAPI(View):
    def get(self,request):
        context = {'movies':self.get_api_data(request)}
        return render(request,'main/movies_list_api.html',context)
    
    #Site pagination handling next and previous site
    def get_next_page(self,page):
        page += 1
        return page

    def get_previous_page(self,page):
        page -= 1
        if page == 0:
            page = 1
        return page
    
    # Method handling search input for movie searching in api
    def get_query_api(self, request):
        query = request.GET.get('query')
        api_fetch = APIFetcher('https://api.themoviedb.org/3', f'/search/movie?api_key=fa16995ba428cf9d86c0d548254c7ffe&query={query}')
        movies_data = api_fetch.fetch_data()
        return movies_data

            
    #MOVIES LIST FROM API HANDLING + SITE FUNCIONALITY (PAGINATION,SEARCH INPUT)
    def get_api_data(self,request):
        global page
        if 'next_page' in request.GET:
            page = self.get_next_page(page)
        elif 'last_page' in request.GET:
            page = self.get_previous_page(page)
        
        
        api_fetch = APIFetcher('https://api.themoviedb.org/3',f'/movie/popular?api_key=fa16995ba428cf9d86c0d548254c7ffe&page={page}')
        movies_data = api_fetch.fetch_data()
        print(api_fetch)

        if movies_data:
            movies = movies_data['results']
        else:
            movies = []
                
        
        if 'query' in request.GET:
            movies_data = self.get_query_api(request)
            if movies_data:
                movies = movies_data['results']
            else:
                movies = []
        return movies













#ABSTRACT CLASS WITH FORM VALIDATION
class FormValidation(ABC):
    @abstractmethod
    def form_validation(self,form,success_url,error_msg,success_msg):
        pass

#HOME PAGE RENDERING
class HomePage(View):
    def get(self,request):
        movies = Movie.objects.all()
        context = {'movies':movies}
        return render(request,'main/home.html',context)
    

#REGISTER PAGE HANDLING
class RegisterRequest(FormValidation,View):
    def get(self,request):
        form = NewUserForm()
        context = {'register_form':form}
        return render(request,'main/register.html',context)
    
    def post(self,request):
        form = NewUserForm(request.POST)
        return self.form_validation(form,'login_page','Try again later...','Registration successful')

    def form_validation(self, form, success_url, error_msg, success_msg):
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(self.request,success_msg)
            return redirect(success_url)
        else:
            messages.error(self.request,error_msg)

#LOGIN PAGE HANDLING
class LoginRequest(FormValidation,View):
    def get(self,request):
        form = AuthenticationForm()
        context = {'login_form':form}
        return render(request,'main/login.html',context)
    
    def post(self,request):
        form = AuthenticationForm(request,data=request.POST)
        return self.form_validation(form,'home_page','Try again later...','Login successfull')

    def form_validation(self, form, success_url, error_msg, success_msg):
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(self.request,user)
                messages.success(self.request,success_msg)
                return redirect(success_url)
            else:
                messages.error(self.request.error)
        else:
            messages.error(self.request,error_msg)

#LOGOUT REQUEST HANDLING
class LogoutRequest(View):
    @method_decorator(login_required)
    def get(self,request):
        logout(request)
        return redirect('home_page')
        