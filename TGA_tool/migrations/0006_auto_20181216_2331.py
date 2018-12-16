# Generated by Django 2.1.3 on 2018-12-16 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0005_auto_20181211_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seance',
            name='chapitre',
        ),
        migrations.RemoveField(
            model_name='seance',
            name='cours',
        ),
        migrations.RemoveField(
            model_name='seance',
            name='creneau',
        ),
        migrations.RemoveField(
            model_name='seance',
            name='notions',
        ),
        migrations.RemoveField(
            model_name='seance',
            name='salle',
        ),
        migrations.AlterField(
            model_name='matiere',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matiere', to='TGA_tool.Curriculum', verbose_name='Curriculum'),
        ),
        migrations.DeleteModel(
            name='Seance',
        ),
    ]
