# Generated by Django 2.1.3 on 2019-02-05 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0026_auto_20190205_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eleve',
            name='email',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='id',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='num',
        ),
        migrations.AddField(
            model_name='eleve',
            name='elevepotentiel_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TGA_tool.ElevePotentiel'),
            preserve_default=False,
        ),
    ]
