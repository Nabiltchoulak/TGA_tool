# Generated by Django 2.2 on 2019-05-04 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0023_auto_20190502_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='adresse',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Adresse du client'),
        ),
        migrations.AddField(
            model_name='eleve',
            name='programme',
            field=models.CharField(blank=True, choices=[('DZ', 'Algérien'), ('FR', 'Francais')], max_length=20, null=True, verbose_name='Programme suivi dans les études'),
        ),
    ]