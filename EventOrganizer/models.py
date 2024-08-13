from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Інші поля вашої кастомної моделі користувача

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='Групи, до яких належить цей користувач.',
        verbose_name='групи'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Спеціальні дозволи для цього користувача.',
        verbose_name='дозволи користувача'
    )

    def __str__(self):
        return self.username
# Модель Спікера
class Speaker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='speakers_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Модель Події
class Event(models.Model):
    EVENT_TYPES = [
        ('conference', 'Conference'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        # Додайте інші типи подій, якщо потрібно
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    max_participants = models.PositiveIntegerField()
    speakers = models.ManyToManyField(Speaker, related_name='events')

    def __str__(self):
        return self.title

# Модель Реєстрації на подію
class Registration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

# Модель Квитка
class Ticket(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='ticket')
    ticket_number = models.CharField(max_length=20, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.ticket_number} for {self.registration.event.title}"

# Модель Програми події
class EventProgram(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='programs')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    speaker = models.ForeignKey(Speaker, on_delete=models.SET_NULL, null=True, related_name='programs')

    def __str__(self):
        return f"{self.title} - {self.event.title}"
