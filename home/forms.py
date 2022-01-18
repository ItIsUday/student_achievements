from django import forms
from django.db import transaction
from django.forms import ModelForm

from home.models import Organization, Achievement
from users.models import Student


class AchievementForm(ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'})
    )
    type = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achievement Type'})
    )
    academic_year = forms.IntegerField(
        min_value=2010,
        max_value=2022,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Academic Year'}),
    )
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    certificate = forms.FileField()
    holders = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        help_text='Hold ctrl and select',
        widget=forms.SelectMultiple(attrs={'style': 'max-width:17em'}),
    )
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(),
                                          widget=forms.Select(attrs={'style': 'max-width:17em'})
                                          )

    class Meta:
        model = Achievement
        fields = ["title", "type", "organization", "academic_year", "date", "certificate"]

    @transaction.atomic
    def save(self):
        serial = Achievement.objects.count()
        ach_obj = Achievement.objects.create(
            id='ach' + str(serial + 1),
            title=self.cleaned_data.get("title"),
            type=self.cleaned_data.get("type").capitalize(),
            organization=self.cleaned_data.get("organization"),
            academic_year=self.cleaned_data.get("academic_year"),
            achievement_date=self.cleaned_data.get("date"),
            certificate=self.cleaned_data.get("certificate")
        )
        return ach_obj


class OrganizationForm(ModelForm):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'})
    )
    type = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Type'})
    )

    class Meta:
        model = Organization
        fields = ["name", "type"]
