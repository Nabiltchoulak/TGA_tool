# Generated by Django 2.1.3 on 2018-12-10 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0002_creneau'),
    ]

    operations = [
        migrations.AddField(
            model_name='creneau',
            name='fin',
            field=models.TimeField(blank=True, null=True),
        ),
    ]