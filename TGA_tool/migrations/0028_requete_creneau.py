# Generated by Django 2.1.3 on 2019-02-05 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0027_auto_20190205_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='requete',
            name='creneau',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Creneau', verbose_name='Créneau'),
        ),
    ]
