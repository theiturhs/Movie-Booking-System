from time import sleep
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from rest_framework.decorators import api_view
from .models import SeatStatus, Seat, Show

@transaction.atomic
def book_seats():
    # check show and seat
    # lock seat
    # book or reject seat
    pass

def processPayment():
    sleep(10)
    return True

def checkAvailability(show_id, row, number):
    try:
        seatStatus = SeatStatus.objects.get(show_id=show_id, seat__row=row, seat__number=number)
        return seatStatus.is_available()
    except SeatStatus.DoesNotExist:
        return True

@transaction.atomic
def lockSeats(show_id, row, number):
    try:
        show = Show.objects.get(id=show_id)
        seat = Seat.objects.get(
            screen=show.screen,
            row=row,
            number=number
        )

        seatStatus, _ = SeatStatus.objects.select_for_update().get_or_create(
            show=show,
            seat=seat,
        )

        if seatStatus.is_booked:
            print(f"Seat {row}{number} already BOOKED")
            return False

        is_locked = (
            seatStatus.locked_until
            and seatStatus.locked_until > timezone.now()
        )

        if not is_locked:
            seatStatus.is_locked = True
            seatStatus.locked_until = timezone.now() + timezone.timedelta(minutes=10)
            seatStatus.save()
            print(f"Seat {row}{number} locked successfully")
            return True

        print(f"Seat {row}{number} is already locked")
        return False

    except Exception as e:
        print(f"Seat was not locked due to {e}")
        return False

def completeBooking(show_id, row, number):
    try:
        show = Show.objects.get(id=show_id)
        seat = Seat.objects.get(
            screen=show.screen,
            row=row,
            number=number
        )

        seatStatus = SeatStatus.objects.get(show=show, seat=seat)
        if seatStatus.is_locked and seatStatus.locked_until > timezone.now():
            seatStatus.is_booked = True
            seatStatus.is_locked = False
            seatStatus.locked_until = None
            seatStatus.save()
            print(f"Seat {row}{number} booked successfully")
            return True
        else:
            print(f"Seat {row}{number} was not booked")
            return False
    except Exception as e:
        print(f"Error booking seat {row}{number}: {e}")
        return False

@api_view(['POST'])
def selectSeat(request):
    row = request.data.get('row')
    number = request.data.get('number')
    show_id = request.data.get('show_id')

    state = checkAvailability(show_id, row, number)
    if state:
        locked_seat = lockSeats(show_id, row, number)
        if locked_seat:
            payment_success = processPayment()
            if payment_success:
                bookingStatus = completeBooking(show_id, row, number)
                if bookingStatus:
                    return HttpResponse(f"Seat {row}{number} booked successfully")
    return HttpResponse(f"Seat {row}{number} is not available")