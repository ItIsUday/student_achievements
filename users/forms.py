from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.db import transaction

from users.models import User, Student, Counselor


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        validators=[RegexValidator('(.)+@rvce\.edu\.in', message='Only valid RVCE mail ID allowed')],
        widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'RVCE Email'}),
    )
    usn = forms.CharField(
        max_length=15,
        validators=[RegexValidator('1RV\d\d[A-Z][A-Z][0-4]\d\d', message='Invalid USN')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'USN'}),
    )
    phone = forms.CharField(
        # to add min_length=10 before deploying,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (IN)'}),
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
    )
    counselor = forms.ModelChoiceField(queryset=Counselor.objects.all(),
                                       widget=forms.Select(attrs={'style': 'max-width:17em'})
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
