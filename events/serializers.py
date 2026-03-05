from django.utils import timezone
from rest_framework import serializers
from .models import Event, Registration

class EventSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField(source="organizer.username", read_only=True)
    attendees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_time",
            "location",
            "organizer",
            "organizer_username",
            "capacity",
            "attendees_count",
            "created_at",
        ]
        read_only_fields = ["organizer", "created_at", "attendees_count"]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title is required.")
        return value

    def validate_location(self, value):
        if not value.strip():
            raise serializers.ValidationError("Location is required.")
        return value

    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError("Capacity must be at least 1.")
        return value

    def validate_start_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Event date/time must be in the future.")
        return value

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ["id", "event", "user", "created_at"]
        read_only_fields = ["created_at"]
