from django.contrib import admin
from .models import Concert, Seat, Row

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0  # Số lượng form trống để thêm mới

class RowInline(admin.TabularInline):
    model = Row
    extra = 0

class ConcertAdmin(admin.ModelAdmin):
    inlines = [RowInline, SeatInline]

admin.site.register(Concert, ConcertAdmin)
