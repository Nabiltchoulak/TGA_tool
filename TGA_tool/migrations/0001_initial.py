# Generated by Django 2.1.3 on 2018-12-09 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapitre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapitre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'chapitre',
            },
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponibilité', models.CharField(blank=True, max_length=15)),
                ('nom', models.CharField(max_length=42, unique=True, verbose_name='Nom')),
                ('telphone', models.CharField(max_length=15, unique=True, verbose_name='Telephone')),
                ('mail', models.EmailField(max_length=254, verbose_name='E-mail')),
            ],
            options={
                'verbose_name': 'coach',
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
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('niveau', models.CharField(max_length=13)),
                ('programme', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Eleve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=42, verbose_name='Nom')),
                ('num', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telephone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('date_naissance', models.DateField(null=True, verbose_name='Date de naissance')),
                ('etablissement', models.CharField(max_length=20, null=True)),
                ('date_inscription', models.DateField(auto_now=True, verbose_name="Date d'inscription")),
                ('cours', models.ManyToManyField(blank=True, related_name='cours', to='TGA_tool.Cours', verbose_name='Cours')),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Curriculum', verbose_name='Curriculum')),
            ],
            options={
                'verbose_name': 'eleve',
            },
        ),
        migrations.CreateModel(
            name='Frequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequence', models.CharField(choices=[('Frequence', (('Une seance', 'Une séance'), ('Chaque jour', 'Chaque jour'), ('Un jour chaque semaine', 'Un jour chaque semaine'), ('Un jour chaque mois', 'Un jour chaque mois'))), ('Personalisé', (('Jours', 'Chaque x jours'), ('Semaines', 'Chaque x semaines'), ('Mois', 'Chaque x mois')))], default='Une seance', max_length=30, verbose_name='Fréquence')),
                ('intervalle', models.PositiveIntegerField(blank=True, null=True, verbose_name='intervalle par fréquence')),
                ('jour', models.PositiveIntegerField(blank=True, choices=[(7, 'Dimanche'), (1, 'Lundi'), (2, 'Mardi'), (3, 'Mercredi'), (4, 'Jeudi'), (5, 'Vendredi'), (6, 'Samedi')], null=True)),
                ('day_of_month', models.PositiveIntegerField(blank=True, null=True, verbose_name='Jour du mois')),
                ('date_limite', models.DateField(blank=True, null=True, verbose_name='Fin de la période')),
                ('date_debut', models.DateField(blank=True, null=True, verbose_name='Debut de la période')),
            ],
            options={
                'verbose_name': 'fréquence',
            },
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matiere', models.CharField(max_length=14, verbose_name='Matiere')),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Curriculum', verbose_name='Curriculum')),
            ],
            options={
                'verbose_name': 'matiere',
            },
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
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=42, unique=True, verbose_name='Nom')),
                ('num_tel', models.CharField(max_length=15, unique=True, verbose_name='Telephone')),
                ('mail', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('adresse', models.CharField(max_length=150, verbose_name='Adresse')),
                ('estResponsable', models.BooleanField(verbose_name="Responsable de l'enfant")),
                ('date_inscription', models.DateField(auto_now=True, verbose_name="Date d'inscription")),
            ],
            options={
                'verbose_name': 'parent',
            },
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponibilité', models.CharField(blank=True, max_length=15)),
                ('nom', models.CharField(max_length=42, unique=True, verbose_name='Nom')),
                ('capcite', models.PositiveIntegerField(verbose_name='Capacité')),
                ('ecran', models.BooleanField(verbose_name='Posséde un écean')),
                ('batiment', models.BooleanField(verbose_name='TGA')),
            ],
            options={
                'verbose_name': 'salle',
            },
        ),
        migrations.CreateModel(
            name='Seance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('creneau', models.TimeField(blank=True, null=True, verbose_name='Creneau')),
                ('statut', models.CharField(choices=[('PL', 'Planifiée'), ('EF', 'Effectuée'), ('AN', 'Annulée')], default='PL', max_length=2, verbose_name='Statut')),
                ('chapitre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Chapitre', verbose_name='Chapitre')),
                ('cours', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Cours', verbose_name='Cours')),
                ('notions', models.ManyToManyField(blank=True, related_name='Titre', to='TGA_tool.Notions', verbose_name='Notions')),
                ('salle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Salle', verbose_name='Salle')),
            ],
            options={
                'verbose_name': 'seance',
            },
        ),
        migrations.AddField(
            model_name='eleve',
            name='parent_resp',
            field=models.ForeignKey(limit_choices_to={'estResponsable': True}, on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Parent', verbose_name='Parent responsable'),
        ),
        migrations.AddField(
            model_name='eleve',
            name='parent_sec',
            field=models.ForeignKey(blank=True, limit_choices_to={'estResponsable': False}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondaire', to='TGA_tool.Parent', verbose_name='Parent contact'),
        ),
        migrations.AddField(
            model_name='cours',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niv', to='TGA_tool.Curriculum', verbose_name='Curriculum'),
        ),
        migrations.AddField(
            model_name='cours',
            name='frequence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Frequence'),
        ),
        migrations.AddField(
            model_name='cours',
            name='matiere',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='TGA_tool.Matiere', verbose_name='Matiere'),
        ),
        migrations.AddField(
            model_name='coach',
            name='matieres',
            field=models.ManyToManyField(related_name='enseigne', to='TGA_tool.Matiere', verbose_name='matieres'),
        ),
        migrations.AddField(
            model_name='chapitre',
            name='matiere',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Matiere', verbose_name='Matiere'),
        ),
    ]
