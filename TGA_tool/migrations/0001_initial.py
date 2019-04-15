# Generated by Django 2.1.7 on 2019-04-10 23:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapitre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapitre', models.CharField(max_length=50)),
                ('details', models.TextField(blank=True, help_text='Précisions sur le chapitre', null=True)),
            ],
            options={
                'verbose_name': 'chapitre',
                'ordering': ['session', 'chapitre'],
            },
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponibilite', models.CharField(blank=True, max_length=15)),
                ('genre', models.CharField(choices=[('M.', 'Monsieur'), ('Mme.', 'Madame'), ('Mlle', 'Mademoiselle')], default='M.', max_length=10, verbose_name='Civilité')),
                ('prenom', models.CharField(default='', max_length=42, verbose_name='Prénom')),
                ('nom', models.CharField(max_length=42, verbose_name='Nom')),
                ('telephone', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Telephone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='E-mail')),
                ('salaire', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('grade', models.CharField(blank=True, choices=[('Junior', 'Junior'), ('Senior', 'Senior'), ('Excellence', 'Excellence')], default='', max_length=10)),
            ],
            options={
                'verbose_name': 'coach',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coach', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Coach', verbose_name='Coach')),
            ],
            options={
                'verbose_name': 'cours',
                'ordering': ['-langue', 'session'],
            },
        ),
        migrations.CreateModel(
            name='Creneau',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debut', models.TimeField()),
                ('fin', models.TimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'créneau',
            },
        ),
        migrations.CreateModel(
            name='ElevePotentiel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=42, verbose_name='Nom complet')),
                ('num', models.CharField(blank=True, max_length=15, verbose_name='Telephone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
            ],
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=42, verbose_name='Nom de famille')),
                ('adresse', models.CharField(max_length=100, unique=True, verbose_name='Adresse de famille')),
            ],
            options={
                'verbose_name': 'Famille',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Frequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequence', models.CharField(choices=[('Frequence', (('Une seance', 'Une séance'), ('Chaque jour', 'Chaque jour'), ('Un jour chaque semaine', 'Chaque semaine'), ('Un jour chaque mois', 'Chaque mois'))), ('Personalisé', (('Jours', 'Chaque X jours'), ('Semaines', 'Chaque X semaines'), ('Mois', 'Chaque X mois')))], default='Une seance', max_length=30, verbose_name='Fréquence')),
                ('jour', models.PositiveIntegerField(blank=True, choices=[(7, 'Dimanche'), (1, 'Lundi'), (2, 'Mardi'), (3, 'Mercredi'), (4, 'Jeudi'), (5, 'Vendredi'), (6, 'Samedi')], help_text='Le jour de la semaine', null=True, verbose_name='Jour de la semaine')),
                ('day_of_month', models.PositiveIntegerField(blank=True, help_text='Le jour du mois (ex: Chaque 25 du mois)', null=True, verbose_name='Jour du mois')),
                ('period', models.PositiveIntegerField(blank=True, null=True, verbose_name='Chaque')),
                ('date_debut', models.DateField(blank=True, help_text='Date du début du cours', null=True, verbose_name='Debut du cours')),
                ('date_limite', models.DateField(blank=True, help_text='Date de la fin du cours', null=True, verbose_name='Fin du cours')),
                ('creneau', models.ForeignKey(blank=True, help_text='Créneau dans la journée', null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Creneau', verbose_name='Creneau')),
            ],
            options={
                'verbose_name': 'fréquence',
            },
        ),
        migrations.CreateModel(
            name='Langue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('niveau', models.CharField(max_length=13)),
                ('programme', models.CharField(blank=True, max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notion', models.CharField(max_length=50, verbose_name='Notion')),
                ('details', models.TextField(blank=True, null=True, verbose_name='Details')),
                ('chapitre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Chapitre')),
            ],
            options={
                'verbose_name': 'notions',
                'ordering': ['chapitre', 'details'],
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(choices=[('M.', 'Monsieur'), ('Mme.', 'Madame'), ('Mlle', 'Mademoiselle')], default='M.', max_length=10, verbose_name='Civilité')),
                ('prenom', models.CharField(default='', max_length=42, verbose_name='Prénom')),
                ('nom', models.CharField(max_length=42, verbose_name='Nom')),
                ('telephone', models.CharField(blank=True, max_length=40, unique=True, verbose_name='Telephone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('profession', models.CharField(blank=True, max_length=100, verbose_name='Profession')),
                ('estResponsable', models.BooleanField(default=False, verbose_name='Parent principal')),
                ('credit', models.IntegerField(default=0)),
                ('debit', models.IntegerField(default=0)),
                ('solde', models.IntegerField(default=0)),
                ('date_inscription', models.DateField(auto_now=True, verbose_name="Date d'inscription")),
            ],
            options={
                'verbose_name': 'parent',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Payement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'verbose_name': 'Paiement',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Requete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.CharField(blank=True, choices=[('Dimanche', 'Dimanche'), ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')], max_length=70, null=True)),
                ('creneau', models.ManyToManyField(blank=True, to='TGA_tool.Creneau', verbose_name='Créneau')),
            ],
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponibilite', models.CharField(blank=True, max_length=15)),
                ('nom', models.CharField(max_length=42, unique=True, verbose_name='Nom')),
                ('capcite', models.PositiveIntegerField(blank=True, null=True, verbose_name='Capacité')),
                ('ecran', models.BooleanField(verbose_name='Posséde un écean')),
                ('batiment', models.BooleanField(verbose_name='TGA')),
            ],
            options={
                'verbose_name': 'salle',
                'ordering': ['capcite'],
            },
        ),
        migrations.CreateModel(
            name='Seance_Coaching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('statut', models.CharField(choices=[('Planifié', 'Planifiée'), ('Done', 'Effectué'), ('Annulé', 'Annulée')], default='Planifié', max_length=8, verbose_name='Statut')),
                ('chapitre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Chapitre', verbose_name='Chapitre')),
                ('coach', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Coach', verbose_name='Coach')),
                ('creneau', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Creneau', verbose_name='Creneau')),
                ('notions', models.ManyToManyField(blank=True, related_name='tga_tool_seance_coaching_related', to='TGA_tool.Notions', verbose_name='Notions')),
                ('salle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Salle', verbose_name='Salle')),
            ],
            options={
                'verbose_name': 'seance coaching',
                'ordering': ['date', 'creneau'],
            },
        ),
        migrations.CreateModel(
            name='Seance_Cours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('statut', models.CharField(choices=[('Planifié', 'Planifiée'), ('Done', 'Effectué'), ('Annulé', 'Annulée')], default='Planifié', max_length=8, verbose_name='Statut')),
                ('chapitre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Chapitre', verbose_name='Chapitre')),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Cours', verbose_name='Cours')),
                ('creneau', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Creneau', verbose_name='Creneau')),
                ('notions', models.ManyToManyField(blank=True, related_name='tga_tool_seance_cours_related', to='TGA_tool.Notions', verbose_name='Notions')),
                ('salle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Salle', verbose_name='Salle')),
            ],
            options={
                'verbose_name': 'seance cours',
                'ordering': ['date', 'creneau'],
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=30, verbose_name='Session')),
                ('langue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session', to='TGA_tool.Langue', verbose_name='Langue')),
            ],
            options={
                'verbose_name': 'session',
                'ordering': ['-langue', 'session'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('parent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TGA_tool.Parent')),
                ('date_naissance', models.DateField(blank=True, null=True, verbose_name='Date de naissance')),
                ('date_commencement', models.DateField(blank=True, verbose_name='Date de commencement')),
            ],
            options={
                'verbose_name': 'client',
                'ordering': ['nom'],
            },
            bases=('TGA_tool.parent',),
        ),
        migrations.CreateModel(
            name='Eleve',
            fields=[
                ('elevepotentiel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TGA_tool.ElevePotentiel')),
                ('date_naissance', models.DateField(blank=True, null=True, verbose_name='Date de naissance')),
                ('etablissement', models.CharField(blank=True, max_length=20, null=True)),
                ('date_inscription', models.DateField(auto_now=True, verbose_name="Date d'inscription")),
            ],
            options={
                'verbose_name': 'eleve',
                'ordering': ['nom'],
            },
            bases=('TGA_tool.elevepotentiel',),
        ),
        migrations.AddField(
            model_name='seance_coaching',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Session'),
        ),
        migrations.AddField(
            model_name='requete',
            name='eleve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.ElevePotentiel'),
        ),
        migrations.AddField(
            model_name='requete',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Session'),
        ),
        migrations.AddField(
            model_name='payement',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Parent', verbose_name='Parent payeur'),
        ),
        migrations.AddField(
            model_name='parent',
            name='famille',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Famille', verbose_name='Famille'),
        ),
        migrations.AddField(
            model_name='parent',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='elevepotentiel',
            name='sessions',
            field=models.ManyToManyField(blank=True, through='TGA_tool.Requete', to='TGA_tool.Session', verbose_name='Cours potentiels demandes'),
        ),
        migrations.AddField(
            model_name='cours',
            name='frequence',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Frequence'),
        ),
        migrations.AddField(
            model_name='cours',
            name='langue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langue', to='TGA_tool.Langue', verbose_name='Langue'),
        ),
        migrations.AddField(
            model_name='cours',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Session', verbose_name='Session'),
        ),
        migrations.AddField(
            model_name='coach',
            name='sessions',
            field=models.ManyToManyField(help_text='Les matières que peut enseigner ce coach', related_name='enseigne', to='TGA_tool.Session', verbose_name='sessions'),
        ),
        migrations.AddField(
            model_name='coach',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chapitre',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Session', verbose_name='Session'),
        ),
        migrations.AddField(
            model_name='seance_cours',
            name='eleves',
            field=models.ManyToManyField(blank=True, related_name='presence', to='TGA_tool.Eleve'),
        ),
        migrations.AddField(
            model_name='seance_coaching',
            name='eleve',
            field=models.ManyToManyField(blank=True, related_name='eleve_coaching', to='TGA_tool.Eleve'),
        ),
        migrations.AddField(
            model_name='requete',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Client'),
        ),
        migrations.AddField(
            model_name='eleve',
            name='cours',
            field=models.ManyToManyField(blank=True, related_name='Eleve_cours', to='TGA_tool.Cours', verbose_name='Cours'),
        ),
        migrations.AddField(
            model_name='eleve',
            name='famille',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Famille', verbose_name='Famille'),
        ),
        migrations.AddField(
            model_name='eleve',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='cours',
            field=models.ManyToManyField(blank=True, related_name='Client_cours', to='TGA_tool.Cours', verbose_name='Cours'),
        ),
        migrations.AddField(
            model_name='client',
            name='sessions',
            field=models.ManyToManyField(blank=True, through='TGA_tool.Requete', to='TGA_tool.Session', verbose_name='Cours potentiels demandes'),
        ),
    ]
