from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from .models import Event, Speaker, Registration, Ticket, EventProgram

User = get_user_model()

class CustomUserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@example.com',
            phone_number='1234567890'
        )

    def test_create_user(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

class SpeakerModelTests(TestCase):

    def setUp(self):
        self.speaker = Speaker.objects.create(
            first_name='John',
            last_name='Doe',
            bio='Expert in Django'
        )

    def test_speaker_creation(self):
        self.assertEqual(Speaker.objects.count(), 1)
        self.assertEqual(self.speaker.first_name, 'John')

    def test_speaker_str(self):
        self.assertEqual(str(self.speaker), 'John Doe')

class EventModelTests(TestCase):

    def setUp(self):
        self.speaker = Speaker.objects.create(
            first_name='Jane',
            last_name='Doe',
            bio='Python Enthusiast'
        )

        self.event = Event.objects.create(
            title='Django Conference',
            description='An event for Django enthusiasts',
            event_type='conference',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1),
            location='Online',
            max_participants=100
        )
        self.event.speakers.add(self.speaker)

    def test_event_creation(self):
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(self.event.title, 'Django Conference')

    def test_event_str(self):
        self.assertEqual(str(self.event), 'Django Conference')

class RegistrationModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='participant',
            password='participantpass',
            email='participant@example.com'
        )
        self.event = Event.objects.create(
            title='Python Workshop',
            description='Learn Python',
            event_type='workshop',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1),
            location='Library',
            max_participants=50
        )
        self.registration = Registration.objects.create(
            user=self.user,
            event=self.event,
            is_paid=True
        )

    def test_registration_creation(self):
        self.assertEqual(Registration.objects.count(), 1)
        self.assertTrue(self.registration.is_paid)

    def test_registration_str(self):
        self.assertEqual(str(self.registration), 'participant - Python Workshop')

class TicketModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='ticketuser',
            password='ticketpass',
            email='ticketuser@example.com'
        )
        self.event = Event.objects.create(
            title='Django Workshop',
            description='Learn Django',
            event_type='workshop',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1),
            location='Hall 1',
            max_participants=30
        )
        self.registration = Registration.objects.create(
            user=self.user,
            event=self.event,
            is_paid=True
        )
        self.ticket = Ticket.objects.create(
            registration=self.registration,
            ticket_number='ABC123'
        )

    def test_ticket_creation(self):
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(self.ticket.ticket_number, 'ABC123')

    def test_ticket_str(self):
        self.assertEqual(str(self.ticket), 'Ticket ABC123 for Django Workshop')

class EventProgramModelTests(TestCase):

    def setUp(self):
        self.speaker = Speaker.objects.create(
            first_name='Anna',
            last_name='Smith',
            bio='JavaScript Expert'
        )
        self.event = Event.objects.create(
            title='JS Conference',
            description='A conference for JS lovers',
            event_type='conference',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1),
            location='Auditorium',
            max_participants=200
        )
        self.program = EventProgram.objects.create(
            event=self.event,
            title='Introduction to JavaScript',
            description='Basics of JavaScript',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            speaker=self.speaker
        )

    def test_program_creation(self):
        self.assertEqual(EventProgram.objects.count(), 1)
        self.assertEqual(self.program.title, 'Introduction to JavaScript')

    def test_program_str(self):
        self.assertEqual(str(self.program), 'Introduction to JavaScript - JS Conference')

class EventAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipassword',
            email='apiuser@example.com'
        )
        self.speaker = Speaker.objects.create(
            first_name='Paul',
            last_name='Walker',
            bio='Technology Speaker'
        )
        self.event = Event.objects.create(
            title='Tech Summit',
            description='A summit for tech enthusiasts',
            event_type='conference',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=2),
            location='Tech Center',
            max_participants=300
        )
        self.event.speakers.add(self.speaker)

    def test_event_list_api(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Tech Summit')

    def test_event_detail_api(self):
        response = self.client.get(reverse('event-detail', args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Tech Summit')
        self.assertEqual(response.data['location'], 'Tech Center')

    def test_registration_creation_api(self):
        self.client.login(username='apiuser', password='apipassword')
        data = {
            'user': self.user.id,
            'event': self.event.id,
            'is_paid': True
        }
        response = self.client.post(reverse('registration-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Registration.objects.count(), 1)
        self.assertEqual(Registration.objects.get().user, self.user)

    def test_ticket_generation(self):
        registration = Registration.objects.create(
            user=self.user,
            event=self.event,
            is_paid=True
        )
        ticket = Ticket.objects.create(
            registration=registration,
            ticket_number='XYZ789'
        )
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(ticket.ticket_number, 'XYZ789')
