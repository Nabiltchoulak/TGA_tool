# Generated by Django 2.1.7 on 2019-04-12 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0009_auto_20190412_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='telephone',
            field=models.CharField(blank=True, max_length=40, verbose_name='Telephone'),
        ),
    ]
