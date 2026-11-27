from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from AccountApp.models import Doctor, Patient

# Create your models here.
class Appointment(models.Model):
    reason=models.TextField(
        max_length=50,
        blank=True)
    prescription=models.FileField(blank=True,upload_to="prescriptions/",validators=[FileExtensionValidator(allowed_extensions=['pdf'],message="accepte uniquement des fichiers pdf")])

    class Status(models.TextChoices):
        PENDING="pending","en attente"
        CONFIRMED="confirmed","confirmé"
        CANCELLED="cancelled","annulé"

        #status=models.CharField(max_length=10,choices=(("pending","en attente"),("confirmed","confirmé"),("cancelled","annulé")),default="pending")
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING)
    duration_minutes=models.PositiveIntegerField(default=30)
    doctor=models.ForeignKey(Doctor,related_name="appointments",on_delete=models.CASCADE)
    patient=models.ForeignKey(Patient,related_name="appointments",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    appointment_date=models.DateTimeField(blank=False)

    def clean(self):
        modified_date=self._state.adding or (Appointment.objects.filter(pk=self.pk,appointment_date=self.appointment_date).exists() )
        if modified_date and self.appointment_date <= timezone.now():
            raise ValidationError("la date du rendez-vous doit etre dans le futur.")

    class Meta():
        ordering=["appointment_date"]
        constraints=[models.UniqueConstraint(
            fields=["doctor","appointment_date"],
            name="unicity_doctor_patient_date",
            violation_error_message="un rdv est deja fixé a cette date pour ce medecin.")]


