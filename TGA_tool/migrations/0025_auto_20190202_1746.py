# Generated by Django 2.1.3 on 2019-02-02 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0024_auto_20190202_0945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payement',
            options={'ordering': ['date'], 'verbose_name': 'Paiement'},
        ),
        migrations.AlterField(
            model_name='seance_coaching',
            name='statut',
            field=models.CharField(choices=[('Planifié', 'Planifiée'), ('Done', 'Effectué'), ('Annulé', 'Annulée')], default='Planifié', max_length=8, verbose_name='Statut'),
        ),
        migrations.AlterField(
            model_name='seance_cours',
            name='statut',
            field=models.CharField(choices=[('Planifié', 'Planifiée'), ('Done', 'Effectué'), ('Annulé', 'Annulée')], default='Planifié', max_length=8, verbose_name='Statut'),
        ),
    ]
