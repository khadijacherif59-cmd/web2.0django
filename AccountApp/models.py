from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator,RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.

number_validator=RegexValidator(
    regex=r'^\d{8}$',
    message="doit contenir exactement 8 chiffres"
)

def birth_date_validator(date):
    if date>=timezone.localdate():
        raise ValidationError("la date doit etre inferieur a celle d'aujourd'hui")

class User (AbstractUser):
    pass

class Doctor(User):
    license_number=models.CharField(max_length=6,unique=True,blank=False,validators=[MinLengthValidator(6)])
    phone=models.CharField(max_length=8,unique=True,validators=[number_validator])
    specialties=models.ManyToManyField('AccountApp.Specialty',related_name="Doctors")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta():
        verbose_name="Doctor"
        verbose_name_plural="Doctors"
    def __str__(self):
        return f"DR. {self.first_name} {self.last_name}"

class Patient(User):
    national_id=models.CharField(max_length=8,unique=True)
    phone=models.CharField(max_length=8,unique=True)
    birth_date=models.DateField(validators=[birth_date_validator])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta():
        verbose_name="Patient"
        verbose_name_plural="Patients"

class Specialty(models.Model):
    name=models.CharField(max_length=50,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta():
        verbose_name="Specialty"
        verbose_name_plural="Specialties"
    def __str__(self):
        return f"{self.name}"
