# Generated by Django 2.1.3 on 2018-11-25 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0003_eleve_groupe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupe',
            name='niveau',
            field=models.CharField(max_length=13),
        ),
    ]
