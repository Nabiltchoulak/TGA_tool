# Generated by Django 2.1.3 on 2018-12-20 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0011_remove_cours_frequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='frequence',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Frequence'),
        ),
    ]
