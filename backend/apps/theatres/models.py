from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Theatre(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='theatres')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.city.name})"

class Screen(models.Model):
    name = models.CharField(max_length=100)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='screens')

    def __str__(self):
        return f"{self.name} - {self.theatre.name}"

class Movie(models.Model):
    name = models.CharField(max_length=100)
    rating = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.name

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='shows')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('movie', 'screen', 'date', 'start_time')

    def __str__(self):
        return f"{self.movie.name} - {self.screen.name} ({self.date} {self.start_time})"

class Seat(models.Model):
    ROW_CHOICES = [(chr(i), chr(i)) for i in range(ord('A'), ord('L') + 1)]
    SEAT_TYPE_CHOICES = [('gold', 'Gold'), ('silver', 'Silver'), ('platinum', 'Platinum')]

    row = models.CharField(max_length=1, choices=ROW_CHOICES)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    seat_type = models.CharField(max_length=15, choices=SEAT_TYPE_CHOICES)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='seats')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('row', 'number', 'screen')

    def __str__(self):
        return f"{self.row}{self.number} ({self.seat_type})"

    def get_seat_label(self):
        return f"{self.row}{self.number}"

class SeatStatus(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seat_statuses')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='seat_statuses')
    is_booked = models.BooleanField(default=False)
    locked_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('show', 'seat')

    def __str__(self):
        status = "Booked" if self.is_booked else "Available"
        return f"{self.seat.get_seat_label()} - {status} ({self.show})"
    
    def is_locked(self):
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False
    
    def is_available(self):
        return not self.is_booked and not self.is_locked()