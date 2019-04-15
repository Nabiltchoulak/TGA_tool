# Generated by Django 2.1.7 on 2019-04-11 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0002_auto_20190411_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payement',
            name='client',
        ),
        migrations.AddField(
            model_name='payement',
            name='parent',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Parent', verbose_name='Client'),
            preserve_default=False,
        ),
    ]
