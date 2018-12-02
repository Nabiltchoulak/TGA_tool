# Generated by Django 2.1.3 on 2018-11-26 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TGA_tool', '0009_fils_pere'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enfant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=10)),
                ('fils', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TGA_tool.Fils')),
            ],
        ),
    ]
