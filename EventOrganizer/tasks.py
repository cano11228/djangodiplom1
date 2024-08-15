from celery import shared_task
import random
import string
from django.core.mail import send_mail


@shared_task
def generate_ticket(user_email, event_name):
    ticket_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    send_mail(
        'Your Ticket for ' + event_name,
        f'Your ticket code is {ticket_code}.',
        'yra06052005@gmail.com',
        [user_email],
        fail_silently=False,
    )

    return ticket_code
