# Generated by Django 2.1.3 on 2019-02-01 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0021_payement'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='solde',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
