# create_sample_data.py
from booking.models import Concert, Seat
from django.utils import timezone

def create_sample_data():
    # Tạo một Concert
    concert = Concert(name="My Concert", date=timezone.now())
    concert.save()

    # Thêm các ghế cho Concert đó
    Seat.objects.create(concert=concert, seat_number="A1")
    Seat.objects.create(concert=concert, seat_number="A2")
    Seat.objects.create(concert=concert, seat_number="B1")
    # Thêm các ghế khác nếu cần

# Gọi hàm để thực thi khi tệp được chạy
if __name__ == "__main__":
    create_sample_data()
