# Generated by Django 2.1.3 on 2018-12-10 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creneau',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debut', models.TimeField()),
            ],
            options={
                'verbose_name': 'créneau',
            },
        ),
    ]