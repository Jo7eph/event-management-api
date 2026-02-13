from django.contrib import admin
from .models import Event, Registration, WaitEvent

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "location", "organizer", "capacity", "created_at")
    search_fields = ("title", "location", "organizer__username")
    list_filter = ("start_time", "location")

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "created_at")
    search_fields = ("event__title", "user__username")

@admin.register(WaitEvent)
class WaitEventAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "created_at")
    search_fields = ("event__title", "user__username")
