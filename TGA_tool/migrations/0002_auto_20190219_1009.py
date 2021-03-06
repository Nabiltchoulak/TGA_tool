# Generated by Django 2.1.3 on 2019-02-19 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequence',
            name='day_of_month',
            field=models.PositiveIntegerField(blank=True, help_text='Le jour du mois (ex: Chaque 25 du mois)', null=True, verbose_name='Jour du mois'),
        ),
        migrations.AlterField(
            model_name='frequence',
            name='jour',
            field=models.PositiveIntegerField(blank=True, choices=[(7, 'Dimanche'), (1, 'Lundi'), (2, 'Mardi'), (3, 'Mercredi'), (4, 'Jeudi'), (5, 'Vendredi'), (6, 'Samedi')], help_text='Le jour de la semaine', null=True, verbose_name='Jour de la semaine'),
        ),
        migrations.AlterField(
            model_name='frequence',
            name='period',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Chaque'),
        ),
        migrations.AlterField(
            model_name='seance_cours',
            name='eleves',
            field=models.ManyToManyField(blank=True, related_name='presence', to='TGA_tool.Eleve'),
        ),
    ]
