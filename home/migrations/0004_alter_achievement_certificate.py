# Generated by Django 4.0 on 2021-12-20 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_achievement_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='certificate',
            field=models.FileField(upload_to='certificates/'),
        ),
    ]
