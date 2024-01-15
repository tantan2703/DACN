from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Concert(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

    def create_seats(self, total_rows, seats_per_row):
        existing_seats = self.seats.all()
        if not existing_seats.exists():
            new_seats = []

            for row_num in range(1, total_rows + 1):
                row_name = f"Row{row_num}"
                row = Row(concert=self, name=row_name, seats_per_row=seats_per_row)
                row.save()

                for seat_number in range(1, seats_per_row + 1):
                    seat_number_str = str(seat_number).zfill(2)
                    seat_number_str = f'S{seat_number_str}'

                    new_seat = Seat(concert=self, seat_number=f"{row_name}-{seat_number_str}")
                    new_seats.append(new_seat)

            Seat.objects.bulk_create(new_seats)

class Row(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='rows')
    name = models.CharField(max_length=255)
    seats_per_row = models.IntegerField(default=20)

    def __str__(self):
        return f"{self.concert.name} - {self.name}"

class Seat(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10, unique=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.concert.name} - {self.seat_number}"

@receiver(post_save, sender=Concert)
def create_seats_for_concert(sender, instance, created, **kwargs):
    if created:
        instance.create_seats(total_rows=10, seats_per_row=20)  # Thay đổi số hàng và số ghế mỗi hàng tùy ý
