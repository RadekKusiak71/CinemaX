from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserProfile, Movie, Room,Seat,Ticket

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	firstname = forms.CharField(max_length=255,required=True)
	lastname = forms.CharField(max_length=255,required=True)
	
	class Meta:
		model = User
		fields = ("username",'firstname','lastname', "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	

class MovieCreationForm(ModelForm):
	class Meta:
		model = Movie
		fields =  ('date','time','language','ticket_price','room')
		labels = {
			'date' : 'Movie date (year-month-day)',
			'hour' : 'Movie hour (hour:minutes:seconds)',
			'ticket_price' : 'Enter ticket price',
			'room' : 'Choose a room'
		}
