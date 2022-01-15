from django.db import models


class Organization(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True)
    name = models.CharField(max_length=255,unique=True)
    type = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Achievement(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    achievement_date = models.DateField()
    type = models.CharField(max_length=30, null=True)
    academic_year = models.PositiveSmallIntegerField()
    certificate = models.FileField(upload_to ='certificates/')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.title}"
