# Generated by Django 2.1.3 on 2018-12-07 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0004_auto_20181206_2224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='frequence',
            old_name='times',
            new_name='intervalle',
        ),
        migrations.AddField(
            model_name='frequence',
            name='date_debut',
            field=models.DateField(blank=True, null=True, verbose_name='Debut de la période'),
        ),
        migrations.AddField(
            model_name='frequence',
            name='date_limite',
            field=models.DateField(blank=True, null=True, verbose_name='Fin de la période'),
        ),
        migrations.AddField(
            model_name='frequence',
            name='day_of_month',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Jour du mois'),
        ),
        migrations.AddField(
            model_name='frequence',
            name='jour',
            field=models.CharField(blank=True, choices=[('Dimanche', 'Dimanche'), ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')], max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='frequence',
            name='frequence',
            field=models.CharField(choices=[('Frequence', (('Une seance', 'Une séance'), ('Chaque jour', 'Chaque jour'), ('Chaque jour de la semaine', 'Chaque jour de la semaine'), ('Chaque jour du mois', "Chaque 'jour' du mois"))), ('Personalisé', (('Jours', 'Chaque x jours'), ('Semaines', 'Chaque x semaines'), ('Mois', 'Chaque x mois')))], default='Une seance', max_length=11, verbose_name='Fréquence'),
        ),
    ]