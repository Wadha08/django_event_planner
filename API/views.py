from django.shortcuts import render
from rest_framework.generics import ListAPIView, DestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView,CreateAPIView
from datetime import datetime
from events.models import Event,Booking
from .serializers import (EventListSerializer, BookingListSerializer,RegisterSerializer, 
	CreateEventSerializer, EventDetailSerializer)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner


class EventList(ListAPIView):
	queryset = Event.objects.filter(date__gte=datetime.today())
	serializer_class = EventListSerializer


class OrgList(ListAPIView):
	queryset = Event.objects.all()
	serializer_class = EventListSerializer
	
	def get_queryset(self):
		return Event.objects.filter(owner__id= self.kwargs['owner_id'])


class BookingList(ListAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingListSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Booking.objects.filter(user=self.request.user)


class Register(CreateAPIView):
	serializer_class = RegisterSerializer

class CreateEvent(CreateAPIView):
	serializer_class = CreateEventSerializer
	permission_classes = [IsAuthenticated]
	
	def perform_create(self,serializer):
		serializer.save(owner=self.request.user)


class UpdateEvent(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = CreateEventSerializer
	permission_classes = [IsAuthenticated,IsOwner]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'


class EventDetails(RetrieveAPIView):
	serializer_class = EventDetailSerializer
	permission_classes = [IsAuthenticated, IsOwner]

	def get_queryset(self,**kwargs):
		return Booking.objects.filter(event__id=self.kwargs['event_id'])





