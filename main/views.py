
import requests
from abc import ABC ,abstractmethod
from decimal import Decimal

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

from .forms import NewUserForm, MovieCreationForm, TicketReservation
from .models import UserProfile,Room,Movie,Seat,Ticket

#GLOBAL VARIABLES
page = 1
date_today = date.today()

#ABSTRACT CLASS WITH FORM VALIDATION
class FormValidation(ABC):
    @abstractmethod
    def form_validation(self):
        pass

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
    
#HOME PAGE RENDERING
class HomePage(View):
    def get(self,request):
        cheapest_movies = self.get_cheapest_movies()
        movies = Movie.objects.all()
        context = {'movies':movies,'ordered_movies':cheapest_movies}
        return render(request,'main/home.html',context)
    
    def get_cheapest_movies(self):
        movies = Movie.objects.all().order_by('-ticket_price')[0:2]
        return movies
    
#REGISTER PAGE HANDLING
class RegisterRequest(FormValidation,View):
    def get(self,request):
        form = NewUserForm()
        context = {'register_form':form}
        return render(request,'main/register.html',context)
    
    def post(self,request):
        form = NewUserForm(request.POST)
        return self.form_validation(form,'login_page','Try again later...','Registration successful')

    # FORM VALIDATION FOR REGISTER PAGE
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
    
    #FORM VALIDATION FOR LOGIN PAGE
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
                return redirect('login_page')
        else:
            messages.error(self.request,error_msg)
            return redirect('login_page')
        
#LOGOUT REQUEST HANDLING
class LogoutRequest(View):
    @method_decorator(login_required)
    def get(self,request):
        logout(request)
        return redirect('home_page')
    
# PAGE WITH MOVIE LIST FROM API
class MovieListAPI(View):
    def get(self,request):
        context = {'movies':self.get_api_data(request)}
        return render(request,'main/movies_list_api.html',context)
    
    #Site pagination handling next and previous site
    @staticmethod
    def get_next_page(page):
        page += 1
        return page
    
    @staticmethod
    def get_previous_page(page):
        page -= 1
        if page == 0:
            page = 1
        return page
    
    # Method handling search input for movie searching in api
    @staticmethod
    def get_query_api(request):
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
        
        #Fetching data
        api_fetch = APIFetcher('https://api.themoviedb.org/3',f'/movie/popular?api_key=fa16995ba428cf9d86c0d548254c7ffe&page={page}')
        movies_data = api_fetch.fetch_data()

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
    
# MOVIE CREATOR PAGE 
class MovieCreator(FormValidation,View):
    # Page render with pk taken from url
    def get(self,request,pk):
        form = MovieCreationForm()
        context = {'movie':self.get_api_data(pk,'fa16995ba428cf9d86c0d548254c7ffe'),'movie_creation_form':form}
        return render(request,'main/movie_creator.html',context)
    
    #Method to fetch api data
    def get_api_data(self,pk, api_key):
        api_fetch = APIFetcher('https://api.themoviedb.org/3', f'/movie/{pk}?api_key={api_key}')
        movie = api_fetch.fetch_data()        
        return movie
    
    #Method to check room status
    @staticmethod
    def get_room_status(room,time):
        return Movie.objects.filter(room=room,time=time).exists()
    
    #Method to retrive data from form
    def get_form_dict(self,form):
        time = form.cleaned_data['time']
        date = form.cleaned_data['date']
        room = form.cleaned_data['room']
        ticket_price = form.cleaned_data['ticket_price']
        language = form.cleaned_data['language']

        form_dict = {
            'time': time,
            'date': date,
            'room': room,
            'ticket_price': ticket_price,
            'language': language
        }

        return form_dict
    
    # Form handling
    @method_decorator(staff_member_required)
    def post(self,request,pk):
        form = MovieCreationForm(request.POST)
        return self.form_validation(form,'home_page','movie_creator_page','Room is taken already...','You have successfuly created a movie',pk)
    #Custom form_validation
    def form_validation(self, form, success_url, error_url,error_msg, success_msg,pk):
        if form.is_valid():
            form_data = self.get_form_dict(form)
            movie = self.get_api_data(pk,'fa16995ba428cf9d86c0d548254c7ffe')
            print(movie['popularity'])
            if self.get_room_status(form_data['room'],form_data['time']):
                messages.error(self.request,error_msg)
                return redirect(error_url,pk)
            else: # IF ROOM IS NOT TAKEN AT SAME TIME WE INPUT IN FORM WE CREATING OBJECT
                poster = movie["poster_path"]
                Movie.objects.create(
                    title = movie['original_title'],
                    date = form_data['date'],
                    time = form_data['time'],
                    image = f'https://image.tmdb.org/t/p/w500/{poster}',
                    duration = movie['runtime'],
                    adult = movie['adult'],
                    description = movie['overview'],
                    popularity = movie['popularity'],
                    ticket_price = form_data['ticket_price'],
                    room = form_data['room'],
                    )
                messages.success(self.request,success_msg)
                return redirect(success_url)
        else:
            messages.error(self.request,error_msg)
#CREATED MOVIES PAGE
class MoviesCreated(View):
    date_today = datetime.now().date()

    def get(self, request):
        movies = Movie.objects.all()
            
        if 'last_day' in request.GET:
            self.get_previous_day()
        elif 'next_day' in request.GET:
            self.get_next_day()
        elif 'search_date' in request.GET:
            self.get_date()

        context = {'movies': movies, 'today': MoviesCreated.date_today}
        return render(request, 'main/movies_created.html', context)

    #DATE CHANGING METHODS
    @staticmethod
    def get_next_day():
        MoviesCreated.date_today += timedelta(days=1)

    @staticmethod
    def get_previous_day():
        if MoviesCreated.date_today == datetime.now().date():
            pass
        else:
            MoviesCreated.date_today -= timedelta(days=1)


    #HANDLING SEARCH BY CALENDAR ALSO CHANGING FORMAT OF DATE FOR YEAR - MOTH - DAY
    def get_date(self):
        date = self.request.GET.get('search_date')
        current_date = datetime.now().date()
        
        if date is None or date < str(current_date):
            date = str(current_date)

        MoviesCreated.date_today = datetime.strptime(date, '%Y-%m-%d').date()

    #DELETING MOVIE
    @method_decorator(staff_member_required)
    def post (self, request):
        movie_id = request.POST.get('movie_id')
        Movie.objects.filter(id=int(movie_id)).delete()
        return redirect('movies_page')

#SEAT RESERVATION
class MovieRoom(View):
    def get(self,request,movie_id):
        movie = Movie.objects.get(id = movie_id)
        room = self.get_taken_seats(movie_id)
        context = {'movie':movie,'range':range(1,7),'room':room}
        return render(request,'main/movie_seat_reservation.html',context)
    
    # Getting room 6x6 method
    @staticmethod
    def get_room():
        room = []
        for row in range(1, 7):
            row_seats = []
            for seat in range(1, 7):
                row_seats.append([row,seat])
            room.append(row_seats)
        return room
    
    # Using method get_room() to take room and then changing taken seats index for 0 
    def get_taken_seats(self, movie_id):
        movie = Movie.objects.get(id=movie_id)
        room = self.get_room()
        seats = Seat.objects.filter(movie=movie)
        if seats:
            for taken_seat in seats:
                room[taken_seat.row_number - 1][taken_seat.seat_number - 1] = 0
        return room
        
#PAGE TO TYPE IN RESERVATION DATA
class ReservationPage(FormValidation,View):
    def get(self,request,seat_num,row_num,movie_id):
        movie = Movie.objects.get(id=movie_id)
        form =TicketReservation()
        context = {'movie':movie,'seat_num':seat_num,'row_num':row_num,'Reservation_form':form}
        return render(request,'main/reservation_page.html',context)
    
    # Method to return price
    @staticmethod
    def get_status_price(status,price):
        if status == 'Student':
            price *= 0.37
        elif status == 'Junior':
            price *= 0.5
        elif status == 'Senior':
            price *= 0.6
        return price
        
    # Validating and saving reservation form
    def post(self,request,movie_id,seat_num,row_num):
        form = TicketReservation(request.POST)
        return self.form_validation(form,'reservation_details_page','Something went wrong, Try again later...',
                                    'Your reservation has been created...',movie_id,seat_num,row_num)
    
    # Form validating with ticket object creating
    def form_validation(self, form, success_url, error_msg, success_msg,movie_id,seat_num,row_num):
        if form.is_valid():
            movie = Movie.objects.get(id=movie_id)
            seat = Seat.objects.create(movie=movie,seat_number=seat_num,row_number=row_num,is_taken=True)
            ticket = form.save(commit=False)
            ticket.seat = seat
            ticket.movie = movie
            ticket.ticket_price = self.get_status_price(ticket.status,movie.ticket_price)
            ticket.save()
            messages.success(self.request,success_msg)
            return redirect(success_url,ticket.id)
        else:
            messages.error(self.request,error_msg)
        
#PAGE TO CONFIRM RESERVATION DETAILS BY USER
class ReservationDetailsPage(View):
    def get(self,request,ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        context = {'ticket':ticket}
        return render(request,'main/reservation_details.html',context)
    # Mail sending method
    @staticmethod
    def mail_sending(message,mail,success_url):
        send_mail(
            "Cinema ticket details",
            message,
            'radoslawkusiak12@gmail.com',
            [mail],
            fail_silently=True,
            )
        return redirect(success_url)
    
    # Method handling confirming and canceling user reservation
    def post(self,request,ticket_id):
        if request.method == 'POST':
            ticket = Ticket.objects.get(id=ticket_id)
            if 'confirm_reservation' in request.POST:
                message = f'Hello {ticket.firstname} {ticket.lastname} this is your ticket for a {ticket.movie.title}\n Seat number {ticket.seat.seat_number} row {ticket.seat.row_number} in room number {ticket.movie.room.number}'
                return self.mail_sending(message,ticket.email,'home_page')
            if 'cancel_reservation' in request.POST:
                ticket.delete()
                return redirect('home_page')
              
class MovieReservationsAdmin(ReservationPage,View):

    def get(self,request,movie_id):
        movie = Movie.objects.get(id=movie_id)
        tickets = Ticket.objects.filter(movie=movie)
        context = {'movie':movie,'tickets':tickets}
        return render(request,'main/movie_reservations.html',context)
    
    @staticmethod
    def mail_sending(title,message,mail,success_url,movie_id):
        send_mail(
            title,
            message,
            'radoslawkusiak12@gmail.com',
            [mail],
            fail_silently=True,
            )
        return redirect(success_url,movie_id)
    
    @method_decorator(staff_member_required)   
    def post(self,request,movie_id):
        ticket = Ticket.objects.get(movie = Movie.objects.get(id=movie_id))
        if request.method == 'POST':
            if 'reservation_mail_broadcast' in request.POST:
                try:
                    message = f'You ticket for movie: {ticket.movie.title} is waiting for confirmation.'
                    return self.mail_sending(
                        'Cinema notification',
                        message,
                        ticket.email,
                        'movie_reservations_admin',
                        ticket.movie.id
                        )
                except ticket.DoesNotExist:
                    pass
            
            if 'reservation_cancel_admin' in request.POST:
                try:
                    ticket.delete()
                    return redirect('movie_reservations_admin',ticket.movie.id)
                except ticket.DoesNotExist:
                    pass
