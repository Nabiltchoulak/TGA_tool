# Generated by Django 2.1.3 on 2019-02-05 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0033_auto_20190205_1951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eleve',
            name='cours',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='curriculum',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='elevepotentiel_ptr',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='famille',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='user',
        ),
        migrations.RemoveField(
            model_name='seance_coaching',
            name='eleve',
        ),
        migrations.RemoveField(
            model_name='seance_cours',
            name='eleves',
        ),
        migrations.DeleteModel(
            name='Eleve',
        ),
    ]
