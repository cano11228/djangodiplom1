from rest_framework import viewsets
from .models import Event, Speaker, Registration, Ticket
from .serializers import EventSerializer, SpeakerSerializer, RegistrationSerializer, TicketSerializer
from .tasks import generate_ticket
from django.shortcuts import render

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


def register_user(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        event_name = 'Sample Event'

        # Виклик асинхронного таску для генерації квитка
        generate_ticket.delay(user_email, event_name)

        return render(request, 'registration_success.html')

    return render(request, 'register.html')