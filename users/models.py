from django.contrib.auth.models import AbstractUser
from django.db import models

from home.models import Achievement


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_counselor = models.BooleanField(default=False)


class Counselor(models.Model):
    type = "Counselor"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    id = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id} - {self.user.get_full_name().title()}"


class Student(models.Model):
    type = "Student"
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    usn = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    achievements = models.ManyToManyField(Achievement, blank=True, related_name="holders")

    def __str__(self):
        return f"{self.usn} - {self.user.get_full_name().title()}"
