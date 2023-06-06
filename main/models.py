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
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    image = models.URLField()
    duration = models.PositiveIntegerField()
    original_language = models.CharField(max_length=32)
    adult = models.BooleanField()
    description = models.TextField(max_length=255)
    popularity = models.DecimalField(decimal_places=2,max_digits=6)
    ticket_price = models.FloatField(default=20.00)
    room = models.ForeignKey('Room',default=None,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title}, date: {self.date} / {self.time} '

class Room(models.Model):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(default=64)

    def __str__(self) -> str:
        return f'Room number {self.number}'
    
class Seat(models.Model):
    seat_number = models.PositiveIntegerField(validators=[MaxValueValidator(8), MinValueValidator(1)])
    row_number = models.PositiveIntegerField(validators=[MaxValueValidator(8), MinValueValidator(1)])
    is_taken = models.BooleanField(default=False)
    movie = models.ForeignKey('Movie',on_delete=models.CASCADE)
    room = models.ForeignKey('Room',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Seat {self.seat_number} \ Row {self.row} \ Movie ID {self.movie.id}'
    
class Ticket(models.Model):
    class PersonStatus(models.TextChoices):
        STUDENT = 'ST',_('Student')
        JUNIOR = 'JR',_('Junior')
        SENIOR = 'SR',_('Senior')
        NORMAL = 'NR',_('Normal')

    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    email = models.EmailField()
    phone = models.CharField(max_length=9)
    status = models.CharField(max_length=7,choices=PersonStatus.choices,default=PersonStatus.NORMAL)

    def __str__(self) -> str:
        return f'Reservation for {self.firstname} {self.lastname} - Status: {self.status}'
