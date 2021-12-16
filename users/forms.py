from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models import query
from django.forms.fields import CharField, DateField
from home.models import Organization

from users.models import User, Student, Counselor


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    usn = forms.CharField(max_length=15)
    phone = forms.CharField(max_length=10)
    birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    counselor = forms.ModelChoiceField(queryset=Counselor.objects.all())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "usn", "phone", "birth_date", "counselor",
                  "password1", "password2"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        Student.objects.create(
            user=user,
            usn=self.cleaned_data.get("usn"),
            phone=self.cleaned_data.get("phone"),
            birth_date=self.cleaned_data.get("birth_date"),
            counselor=self.cleaned_data.get("counselor")
        )
        return user


class CounselorSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    ID = forms.CharField(max_length=15)
    phone = forms.CharField(max_length=10)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "ID", "phone", "password1", "password2"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_counselor = True
        user.save()
        Counselor.objects.create(
            user=user,
            id=self.cleaned_data.get("ID"),
            phone=self.cleaned_data.get("phone")
        )
        return user

class AchievementForm(forms.Form):
    title=forms.CharField(max_length=50)
    date=forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    type=forms.CharField(max_length=20, help_text = "Enter type of achievement")
    academic_year=forms.IntegerField(min_value=2010,max_value=2022)
    certificate=forms.FileField()
    holders=forms.ModelMultipleChoiceField(queryset=Student.objects.all())
    organization=forms.ModelChoiceField(queryset=Organization.objects.all())
