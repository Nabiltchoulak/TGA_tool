# Generated by Django 2.1.3 on 2019-02-09 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0037_coach_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevepotentiel',
            name='nom',
            field=models.CharField(max_length=42, verbose_name='Nom complet'),
        ),
        migrations.AlterField(
            model_name='famille',
            name='adresse',
            field=models.CharField(max_length=100, unique=True, verbose_name='Adresse de famille'),
        ),
        migrations.AlterField(
            model_name='parent',
            name='telephone',
            field=models.CharField(max_length=40, unique=True, verbose_name='Telephone'),
        ),
    ]
