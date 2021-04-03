from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse


class Subject(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('TeacherListView')


class Teacher(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, db_index=True)
    image = models.ImageField(upload_to="images/", null=True, default="images/default.jpg")
    email = models.EmailField(max_length=254, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    room_number = models.CharField(max_length=5, null=True, blank=True)
    subjects = models.ManyToManyField('Subject', related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}" + ' | ' + self.email

    def get_absolute_url(self):
        return reverse('TeacherListView')
