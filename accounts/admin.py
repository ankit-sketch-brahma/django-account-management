from django.contrib import admin
from .models import CustomUser, HOD, Faculity, Student, StudentMark

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(HOD)
admin.site.register(Faculity)
admin.site.register(Student)
admin.site.register(StudentMark)
