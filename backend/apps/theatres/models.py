from statistics import mode
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class City(models.Model):
    cityId = models.IntegerField(primary_key=True, auto_created=True, null=False)
    cityName = models.CharField(max_length=100)
    activeState = models.BooleanField(default=False)

class Theatre(models.Model):
    theatreId = models.IntegerField(primary_key=True, auto_created=True, null=False)
    theatreName = models.CharField(max_length=100)
    activeState = models.BooleanField(default=False)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE)

class Screen(models.Model):
    screenId = models.IntegerField(primary_key=True, auto_created=True, null=False)
    screenName = models.CharField(max_length=100)
    theatreId = models.ForeignKey(Theatre, on_delete=models.CASCADE)

class Movie(models.Model):
    movieId = models.IntegerField(primary_key=True, auto_created=True, null=False)
    movieName = models.CharField(max_length=100)
    startTime = models.TimeField(null=False)
    endTime = models.TimeField(null=False)
    date = models.DateField(null=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    screenId = models.ForeignKey(Screen, on_delete=models.CASCADE)

class Seat(models.Model):
    seatId = models.IntegerField(primary_key=True, auto_created=True, null=False)
    ROW_CHOICES = [(chr(i), chr(i)) for i in range(ord('A'), ord('L') + 1)]
    seatRow = models.CharField(
        max_length=1,
        choices=ROW_CHOICES
    )
    seatNumber = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12)
        ]
    )
    seatType = models.CharField(max_length=15, choices=[('gold', 'Gold'), ('silver', 'Silver'), ('platinum', 'Platinum')])
    screenId = models.ForeignKey(Screen, on_delete=models.CASCADE)
    seatPrice = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def getSeat(self):
        return f"{self.seatRow}{self.seatNumber}"

class SeatStatus(models.Model):
    screenId = models.ForeignKey(Screen, on_delete=models.CASCADE)
    movieID = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seatId = models.ForeignKey(Seat, on_delete=models.CASCADE)
    isBooked = models.BooleanField(default=False)