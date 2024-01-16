# models.py

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Concert(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Row(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='rows')
    name = models.CharField(max_length=255)
    seats_per_row = models.IntegerField(default=20)

    def __str__(self):
        return f"{self.concert.name} - {self.name}"

    def update_seats_per_row(self):
        current_seats = self.seats.count()
        if self.seats_per_row != current_seats:
            self.seats_per_row = current_seats
            self.save()

class Seat(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='seats')
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10, unique=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.concert.name} - {self.seat_number}"

# models.py

# ... (các import và models khác)

@receiver(post_save, sender=Row)
def create_seats_for_row(sender, instance, created, **kwargs):
    # Nếu row mới được tạo hoặc số lượng ghế không bằng với seats_per_row, cập nhật lại ghế
    if created or instance.seats_per_row != instance.seats.count():
        # Xóa tất cả các ghế cũ của row
        instance.seats.all().delete()

        # Tạo mới ghế theo seats_per_row
        new_seats = [
            Seat(concert=instance.concert, row=instance, seat_number=f"{instance.name}-{str(i).zfill(2)}")
            for i in range(1, instance.seats_per_row + 1)
        ]

        # Sử dụng bulk_create để tạo mới danh sách ghế
        Seat.objects.bulk_create(new_seats)

        # Cập nhật seats_per_row trực tiếp trong Row
        instance.update_seats_per_row()

@receiver(post_delete, sender=Seat)
def delete_seat(sender, instance, **kwargs):
    # Kiểm tra xem ghế có đang được đặt chỗ không
    if not instance.is_booked:
        # Lấy danh sách tất cả các ghế của hàng của ghế bị xóa
        seats_to_update = instance.row.seats.all()

        # Sắp xếp danh sách các ghế theo số thứ tự ghế
        sorted_seats = sorted(seats_to_update, key=lambda seat: int(seat.seat_number.split('-')[-1]))

        # Cập nhật lại seatname cho tất cả các ghế theo thứ tự từ 1 đến seat_per_row
        Seat.objects.bulk_update(
            [Seat(pk=seat.pk, seat_number=f"{instance.row.name}-{str(i).zfill(2)}") for i, seat in enumerate(sorted_seats, start=1)],
            fields=['seat_number']
        )

        # Cập nhật seats_per_row trực tiếp trong Row khi xóa ghế
        instance.row.update_seats_per_row()

