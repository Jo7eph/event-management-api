from django.db import transaction
from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Event, Registration, WaitEvent
from .serializers import EventSerializer, RegistrationSerializer
from .permissions import IsOrganizerOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "location"]
    ordering_fields = ["start_time", "created_at"]
    filterset_fields = ["location", "organizer"]


    def get_queryset(self):
        qs = (
            Event.objects
            .select_related("organizer")
            .annotate(attendees_count=Count("registrations"))
        )

        # Upcoming filter toggle
        upcoming = self.request.query_params.get("upcoming")
        if upcoming in ("1", "true", "True"):
            qs = qs.filter(start_time__gt=timezone.now())

        # Date range: start_after / start_before (YYYY-MM-DD)
        start_after = self.request.query_params.get("start_after")
        start_before = self.request.query_params.get("start_before")
        if start_after:
            qs = qs.filter(start_time__date__gte=start_after)
        if start_before:
            qs = qs.filter(start_time__date__lte=start_before)

        return qs

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        qs = self.get_queryset().filter(start_time__gt=timezone.now()).order_by("start_time")
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()

        # Organizer can register too? If you want to forbid:
        # if event.organizer == request.user: return Response(...)

        # Already registered?
        if Registration.objects.filter(event=event, user=request.user).exists():
            return Response({"detail": "Already registered."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Lock event row to avoid race conditions
            event_locked = Event.objects.select_for_update().annotate(attendees_count=Count("registrations")).get(pk=event.pk)

            if event_locked.start_time <= timezone.now():
                return Response({"detail": "Cannot register for past events."}, status=status.HTTP_400_BAD_REQUEST)

            if event_locked.attendees_count >= event_locked.capacity:
                # Optional waitlist
                WaitEvent.objects.get_or_create(event=event_locked, user=request.user)
                return Response({"detail": "Event is full. Added to waitlist."}, status=status.HTTP_200_OK)

            reg = Registration.objects.create(event=event_locked, user=request.user)

        return Response(RegistrationSerializer(reg).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unregister(self, request, pk=None):
        event = self.get_object()

        reg = Registration.objects.filter(event=event, user=request.user).first()
        if reg:
            reg.delete()
            return Response({"detail": "Unregistered successfully."}, status=status.HTTP_200_OK)

        # Also remove from waitlist if present
        WaitEvent.objects.filter(event=event, user=request.user).delete()
        return Response({"detail": "No registration found (removed from waitlist if existed)."}, status=status.HTTP_200_OK)
