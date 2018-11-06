from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    duration = models.DurationField(default=timedelta(minutes=120))
    small_image = models.CharField(max_length=500)
    big_image = models.CharField(max_length=500)
    synopsis = models.TextField(default="")

    def __str__(self):
        return self.name + '(' + self.language + ')'

class Theatre(models.Model):
    name = models.CharField(max_length=100)
    small_image = models.CharField(max_length=500)
    big_image = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Seat(models.Model):  
    rows = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
    columns = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20')
    row_id = models.CharField(max_length=1, choices=zip(rows, rows))
    column_id = models.CharField(max_length=2, choices=zip(columns, columns))

    def __str__(self):
        return self.row_id + self.column_id

class Screen(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    seats = models.ManyToManyField(Seat)
    def __str__(self):
        return self.name + ' (' + self.theatre.name + ')'

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def get_time(self):
        return self.date_time.time().strftime("%I:%M %p")

    def get_date(self):
        return self.date_time.date().strftime("%d-%b-%Y")

    def get_day(self):
        return self.date_time.date().strftime("%A %d")
    
    def get_day_date(self):
        return self.date_time.date().strftime("%A %d, %b %Y")

    def __str__(self):
        return self.movie.name + ' - ' +self.screen.name + ' (' + self.theatre.name + ')' + ' -- ' + self.get_date() + ' ' + self.get_time()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)

    def __str__(self):
        seat_str = ''
        for i in self.seats.all():
            seat_str += str(i) + ', '
        seat_str = seat_str[:-2]
        return self.user.username + ' - ' + self.show.movie.name + '(' + self.show.theatre.name + '-' + self.show.screen.name + ')' + ' -- ' + seat_str