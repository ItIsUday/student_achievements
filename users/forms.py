from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from home.models import Organization, Achievement
from users.models import User, Student, Counselor


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    usn = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'USN'}),
    )
    phone = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (IN)'}),
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
    )
    counselor = forms.ModelChoiceField(queryset = Counselor.objects.all(),
        widget = forms.Select(attrs={'style': 'max-width:17em'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "usn", "phone", "birth_date", "counselor",
                  "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

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
    email = forms.EmailField(
        max_length=254,
        widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    ID = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID'}),
    )
    phone = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (IN)'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "ID", "phone", "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

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


class AchievementForm(ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'})
    )
    type = forms.CharField(
        max_length=20,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achievement Type'})
    )
    academic_year = forms.IntegerField(
        min_value=2010,
        max_value=2022,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Academic Year'}),
    )
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    certificate = forms.FileField()
    holders = forms.ModelMultipleChoiceField(
        queryset = Student.objects.all(),
        help_text = 'Hold ctrl and select',
        widget = forms.SelectMultiple(attrs={'style': 'max-width:17em'}),
        # widget=forms.CheckboxSelectMultiple
    )
    organization = forms.ModelChoiceField(queryset = Organization.objects.all(),
        widget = forms.Select(attrs = {'style': 'max-width:17em'})
    )

    class Meta:
        model = Achievement
        fields = ["title", "type", "organization", "academic_year", "date", "certificate"]

    @transaction.atomic
    def save(self):
        serial = Achievement.objects.count()
        ach_obj = Achievement.objects.create(
            id = 'ach'+str(serial+1),
            title = self.cleaned_data.get("title"),
            type=self.cleaned_data.get("type"),
            organization = self.cleaned_data.get("organization"),
            academic_year = self.cleaned_data.get("academic_year"),
            achievement_date = self.cleaned_data.get("date"),
            certificate = self.cleaned_data.get("certificate")
        )
        return ach_obj
