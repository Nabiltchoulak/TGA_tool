# Generated by Django 2.1.3 on 2019-02-05 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0031_auto_20190205_1939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requete',
            name='creneau',
        ),
        migrations.AddField(
            model_name='requete',
            name='creneau',
            field=models.ManyToManyField(blank=True, null=True, to='TGA_tool.Creneau', verbose_name='Créneau'),
        ),
    ]
