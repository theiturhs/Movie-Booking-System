import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.theatres.models import Seat, Screen

SCREEN_ID = 1

seat_plan = {
    "A": ("platinum", 400),
    "B": ("platinum", 400),
    "C": ("platinum", 400),
    "D": ("gold", 300),
    "E": ("gold", 300),
    "F": ("gold", 300),
    "G": ("silver", 200),
    "H": ("silver", 200),
    "I": ("silver", 200),
    "J": ("silver", 200),
}

screen = Screen.objects.get(id=SCREEN_ID)

seats = []
for row, (seat_type, price) in seat_plan.items():
    for number in range(1, 13):
        seats.append(
            Seat(
                row=row,
                number=number,
                seat_type=seat_type,
                price=price,
                screen=screen
            )
        )

Seat.objects.bulk_create(seats)

print(f"Inserted {len(seats)} seats successfully")