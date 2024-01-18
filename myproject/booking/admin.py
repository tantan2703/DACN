
from django.contrib import admin
from .models import Concert, Row, Seat

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0

class RowInline(admin.TabularInline):
    model = Row
    extra = 0
    inlines = [SeatInline]

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    inlines = [RowInline]

@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    inlines = [SeatInline]