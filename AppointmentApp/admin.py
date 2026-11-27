from django.contrib import admin
from AppointmentApp.models import Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdminPersonnaliser(admin.ModelAdmin):
    pass