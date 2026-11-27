from django.contrib import admin
from AccountApp.models import Doctor,Patient,Specialty,User
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(User)
admin.site.register(Specialty)