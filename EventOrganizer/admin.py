from django.contrib import admin
from .models import Event, Speaker, Registration, Ticket, EventProgram, CustomUser

admin.site.register(Event)
admin.site.register(Speaker)
admin.site.register(Registration)
admin.site.register(Ticket)
admin.site.register(EventProgram)
admin.site.register(CustomUser)
