from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=9,null=True)

    def __str__(self) -> str:
        return f'User: {self.user.username}'
    
class Movie(models.Model):
    class LanguageChoices(models.TextChoices):
        ENGLISH = 'ENG',_('English')
        POLISH = 'POL',_('Polish')
        SUBTITLES = 'ENG-SUB',_('English with polish subtitles')
        DUBBING = 'POL-DUB',_('Polish dubbing')

    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    image = models.URLField()
    duration = models.PositiveIntegerField()
    language = models.CharField(max_length=30,choices=LanguageChoices.choices,default=LanguageChoices.ENGLISH)
    adult = models.BooleanField()
    description = models.TextField(max_length=255)
    popularity = models.DecimalField(decimal_places=2,max_digits=6)
    ticket_price = models.DecimalField(decimal_places=2,max_digits=4,default=20.00)
    room = models.ForeignKey('Room',default=None,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title}, date: {self.date} / {self.time} '

class Room(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        return f'Room number {self.number}'
    
class Seat(models.Model):
    seat_number = models.PositiveIntegerField(validators=[MaxValueValidator(8), MinValueValidator(1)])
    row_number = models.PositiveIntegerField(validators=[MaxValueValidator(8), MinValueValidator(1)])
    is_taken = models.BooleanField(default=False)
    movie = models.ForeignKey('Movie',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Seat {self.seat_number} \ Row {self.row_number} \ Movie ID {self.movie.id}'
    
class Ticket(models.Model):
    class PersonStatus(models.TextChoices):
        STUDENT = 'Student',_('Student')
        JUNIOR = 'Junior',_('Junior')
        SENIOR = 'Senior',_('Senior')
        NORMAL = 'Normal',_('Normal')

    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    email = models.EmailField()
    phone = models.CharField(max_length=9)
    status = models.CharField(max_length=7,choices=PersonStatus.choices,default=PersonStatus.NORMAL)
    movie = models.ForeignKey('Movie',on_delete=models.CASCADE,default=None)
    seat = models.ForeignKey('Seat',on_delete=models.CASCADE,default=None)
    ticket_price = models.DecimalField(decimal_places=2,max_digits=4,default=20.00)
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    
    def __str__(self) -> str:
        return f'Reservation for {self.firstname} {self.lastname} - Status: {self.status}'
